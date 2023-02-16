from booking.models import Booking


def prepare_booking(booking: Booking):
    flights = [booking.flight_from]
    if booking.flight_back:
        flights.append(booking.flight_back)

    return {
        "passengers": booking.passengers,
        "flights": flights,
        "code": booking.code,
        "cost": booking.cost,
    }
