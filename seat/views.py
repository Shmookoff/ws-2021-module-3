from booking.models import Booking
from django.http import Http404
from passenger.serializers import PassengerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookingSeatChoiceRequestSerializer, BookingSeatSerializer
from .services import (
    change_seat,
    is_seat_occupied,
    passenger_in_booking,
    prepare_seat_data,
)


class BookingSeatView(APIView):
    serializer_class = BookingSeatSerializer

    def get_booking(self, code):
        try:
            return Booking.objects.get(code=code)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")

    def get(self, request, code):
        booking = self.get_booking(code)

        data = prepare_seat_data(booking)
        serializer = BookingSeatSerializer(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, code):
        booking = self.get_booking(code)
        r_serializer = BookingSeatChoiceRequestSerializer(data=request.data)
        if r_serializer.is_valid():
            passenger = passenger_in_booking(
                booking, r_serializer.validated_data["passenger"]
            )
            if not passenger:
                return Response(
                    {"error": "Passenger does not apply to booking"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if is_seat_occupied(
                booking,
                r_serializer.validated_data["seat"],
                r_serializer.validated_data["type"],
            ):
                return Response(
                    {"error": "Seat is occupied"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            passenger = change_seat(
                passenger,
                r_serializer.validated_data["seat"],
                r_serializer.validated_data["type"],
            )

            serializer = PassengerSerializer(passenger)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(r_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
