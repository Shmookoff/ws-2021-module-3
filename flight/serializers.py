from django.core.validators import MaxValueValidator, MinValueValidator
from flight_airport.serializers import FlightAirportSerializer
from rest_framework import serializers

from .models import Flight


class FlightQuerySerializer(serializers.Serializer):
    to = serializers.CharField()
    _from = serializers.CharField()
    date1 = serializers.DateField()
    date2 = serializers.DateField(required=False, default=None)
    passengers = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )


FlightQuerySerializer._declared_fields[
    "from"
] = FlightQuerySerializer._declared_fields.pop("_from")


class FlightSerializer(serializers.ModelSerializer):
    flight_id = serializers.IntegerField(source="id")
    flight_code = serializers.CharField(source="code")
    _from = FlightAirportSerializer(source="departure")
    to = FlightAirportSerializer(source="arrival")

    class Meta:
        model = Flight
        fields = (
            "flight_id",
            "flight_code",
            "from",
            "to",
            "cost",
            "availability",
        )


FlightSerializer._declared_fields["from"] = FlightSerializer._declared_fields.pop(
    "_from"
)


class FlightSearchSerializer(serializers.Serializer):
    flights_to = FlightSerializer(many=True)
    flights_back = FlightSerializer(many=True)
