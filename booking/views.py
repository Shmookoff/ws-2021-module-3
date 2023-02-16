from django.db.models import Q
from django.urls import is_valid_path
from django.utils.crypto import get_random_string
from rest_framework import exceptions, status, views
from rest_framework.response import Response

from exceptions import UnproccessableEntity
from flight.models import Flight

from .models import ActualFlight, Booking, Passenger
from .serializers import (
    CreateBookingRequestSerializer,
    GetBookingResponsePassengerSerializer,
    GetBookingResponseSerializer,
    PatchSeatRequestSerializer,
)


class BookingView(views.APIView):
    @staticmethod
    def search_flight(data: dict, key: str):
        flight = Flight.objects.filter(
            Q(departure__date=data[key]["date"]) | Q(departure__date__isnull=True),
            pk=data[key]["id"],
        ).first()
        if not flight:
            raise exceptions.NotFound(f"{key} not found")
        return flight

    @classmethod
    def fetch_actual_flight(cls, data: dict, key: str) -> ActualFlight:
        flight = cls.search_flight(data, key)
        actual_flight, _ = flight.actual_flights.get_or_create(date=data[key]["date"])
        return actual_flight

    @staticmethod
    def check_availability(
        passengers: list, flight_from: ActualFlight, flight_back: ActualFlight | None
    ):
        from_available = flight_from.availability >= len(passengers)
        if flight_back:
            back_available = flight_back.availability >= len(passengers)
            return from_available and back_available
        return from_available

    @staticmethod
    def create_booking(
        passengers: list,
        flight_from: ActualFlight,
        flight_back: ActualFlight | None,
    ):
        flight_from.availability -= len(passengers)
        flight_from.save()
        if flight_back:
            flight_back.availability -= len(passengers)
            flight_back.save()

        return Booking.objects.create(
            code=get_random_string(
                length=5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            flight_from=flight_from,
            flight_back=flight_back,
            cost=(
                flight_from.flight.cost
                + (flight_back.flight.cost if flight_back else 0)
            )
            * len(passengers),
        )

    @staticmethod
    def create_passengers(passengers: list[dict], booking: Booking):
        [
            Passenger.objects.create(**passenger, booking=booking)
            for passenger in passengers
        ]

    def post(self, request: views.Request, **kwargs):
        req_serializer = CreateBookingRequestSerializer(data=request.data)
        if not req_serializer.is_valid():
            raise UnproccessableEntity(req_serializer.errors)

        data: dict = req_serializer.validated_data

        actual_flight_from = self.fetch_actual_flight(data, "flight_from")
        actual_flight_back = (
            self.fetch_actual_flight(data, "flight_back")
            if data.get("flight_back")
            else None
        )

        if not self.check_availability(
            data["passengers"], actual_flight_from, actual_flight_back
        ):
            raise UnproccessableEntity({"passengers": "not enough seats"})

        booking = self.create_booking(
            data["passengers"], actual_flight_from, actual_flight_back
        )

        self.create_passengers(data["passengers"], booking)

        return Response(
            {"code": booking.code},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request: views.Request, code: str):
        booking = Booking.objects.filter(code=code).first()
        if not booking:
            raise exceptions.NotFound("booking not found")

        flights = [booking.flight_from]
        if booking.flight_back:
            flights.append(booking.flight_back)
        serializer = GetBookingResponseSerializer(
            {
                "passengers": booking.passengers,
                "flights": flights,
                "code": booking.code,
                "cost": booking.cost,
            }
        )
        return Response(serializer.data, status.HTTP_200_OK)


class SeatView(views.APIView):
    def get(self, request: views.Request, code: str):
        booking = Booking.objects.filter(code=code).first()
        if not booking:
            raise exceptions.NotFound("booking not found")

        seats = {"occupied_from": [], "occupied_back": []}
        for passenger in booking.passengers.all():
            if passenger.place_from:
                seats["occupied_from"].append(
                    {"passenger_id": passenger.pk, "place": passenger.place_from}
                )
            if passenger.place_back:
                seats["occupied_back"].append(
                    {"passenger_id": passenger.pk, "place": passenger.place_back}
                )
        return Response(seats, status.HTTP_200_OK)

    def patch(self, request: views.Request, code: str):
        booking = Booking.objects.filter(code=code).first()
        if not booking:
            raise exceptions.NotFound("booking not found")

        req_serializer = PatchSeatRequestSerializer(data=request.data)
        if not req_serializer.is_valid():
            raise UnproccessableEntity(req_serializer.errors)

        data: dict = req_serializer.validated_data

        passenger = booking.passengers.filter(pk=data["passenger"]).first()
        if not passenger:
            raise exceptions.PermissionDenied("Passenger does not apply to booking")

        is_seat_occupied = Passenger.objects.filter(
            **{
                f"place_{data['type']}": data["seat"],
                f"booking__flight_{data['type']}": getattr(
                    booking, f"flight_{data['type']}"
                ),
            }
        ).exists()
        if is_seat_occupied:
            raise UnproccessableEntity("Seat is occupied")

        setattr(passenger, f"place_{data['type']}", data["seat"])
        passenger.save()

        serializer = GetBookingResponsePassengerSerializer(passenger)

        return Response(serializer.data, status.HTTP_200_OK)
