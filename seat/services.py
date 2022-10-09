from booking.models import Booking
from django.http import Http404
from flight.models import Flight
from passenger.models import Passenger


def prepare_seat_data(booking: Booking):
    return {
        "occupied_from": [
            {"passenger_id": passenger.id, "place": passenger.place_from}
            for passenger in booking.passengers.all()
        ],
        "occupied_back": [
            {"passenger_id": passenger.id, "place": passenger.place_back}
            for passenger in booking.passengers.all()
            if booking.flight_back
        ],
    }


def is_seat_occupied(booking: Booking, place: str, type: str) -> bool:
    return Passenger.objects.filter(
        **{
            f"place_{type}": place,
            f"booking__flight_{type}": getattr(booking, f"flight_{type}"),
        }
    ).exists()


def passenger_in_booking(booking: Booking, passenger_id: int) -> Passenger | None:
    return booking.passengers.filter(id=passenger_id).first()


def change_seat(passenger: Passenger, place: str, type: str) -> Passenger:
    setattr(passenger, f"place_{type}", place)
    passenger.save()

    return passenger
