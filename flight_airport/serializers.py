from rest_framework import serializers

from .models import FlightAirport


class FlightAirportSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="airport.city.name")
    airport = serializers.CharField(source="airport.name")
    iata = serializers.CharField(source="airport.iata")

    class Meta:
        model = FlightAirport
        fields = ("city", "airport", "iata", "date", "time")
