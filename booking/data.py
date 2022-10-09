import dataclasses
import datetime

from django.db import transaction
from django.db.models import F
from django.utils.crypto import get_random_string
from flight.models import Flight
from passenger.models import Passenger

from .models import Booking


@dataclasses.dataclass
class CreateBookingRequestFlightData:
    id: int
    date: datetime.date


@dataclasses.dataclass
class CreateBookingRequestPassengerData:
    first_name: str
    last_name: str
    birth_date: datetime.date
    document_number: str


@dataclasses.dataclass
class CreateBookingRequestData:
    flight_from: CreateBookingRequestFlightData
    flight_back: CreateBookingRequestFlightData | None
    passengers: list[CreateBookingRequestPassengerData]

    def __post_init__(self):
        if isinstance(self.flight_from, dict):
            self.flight_from = CreateBookingRequestFlightData(**self.flight_from)
        if isinstance(self.flight_back, dict):
            self.flight_back = CreateBookingRequestFlightData(**self.flight_back)
        if isinstance(self.passengers, list):
            self.passengers = [
                CreateBookingRequestPassengerData(**passenger)
                for passenger in self.passengers
                if isinstance(passenger, dict)
            ]

    def get_flights(self):
        return (
            Flight.objects.get(id=self.flight_from.id),
            Flight.objects.get(id=self.flight_back.id) if self.flight_back else None,
        )

    def has_enough_seats(self):
        flight_from, flight_back = self.get_flights()
        from_enough = flight_from.availability >= len(self.passengers)
        if flight_back:
            back_enough = flight_back.availability >= len(self.passengers)
            return from_enough and back_enough
        return from_enough

    @transaction.atomic
    def create(self):
        flight_from, flight_back = self.get_flights()

        booking = Booking.objects.create(
            code=get_random_string(
                length=5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            cost=flight_from.cost + (flight_back.cost if flight_back else 0),
            flight_from=flight_from,
            flight_back=flight_back,
        )

        self._create_passengers(booking)

        return booking

    def _create_passengers(self, booking: Booking):
        passengers = [
            dataclasses.asdict(passenger) | {"booking_id": booking.id}
            for passenger in self.passengers
        ]
        Passenger.objects.bulk_create(
            Passenger(**passenger) for passenger in passengers
        )
        Flight.objects.filter(id=self.flight_from.id).update(
            availability=F("availability") - len(self.passengers)
        )
