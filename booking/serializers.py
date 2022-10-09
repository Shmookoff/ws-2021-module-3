from flight.serializers import FlightSerializer
from passenger.serializers import PassengerCreateSerializer, PassengerSerializer
from rest_framework import serializers

from .models import Booking


class BookingFlightCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # Flight ID
    date = serializers.DateField()


class CreateBookingRequestSerializer(serializers.Serializer):
    flight_from = BookingFlightCreateSerializer()
    flight_back = BookingFlightCreateSerializer()
    passengers = PassengerCreateSerializer(many=True)


class BookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)
    flights = FlightSerializer(many=True)

    class Meta:
        model = Booking
        fields = ("code", "cost", "passengers", "flights")
