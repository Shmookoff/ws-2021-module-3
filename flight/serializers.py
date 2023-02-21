from rest_framework import serializers

from booking.models import ActualFlight

from .models import Flight, FlightJuncture


class FlightQuerySerializer(serializers.Serializer):
    from_ = serializers.CharField()
    to = serializers.CharField()
    date1 = serializers.DateField()
    date2 = serializers.DateField(required=False, default=None)
    passengers = serializers.IntegerField(min_value=1, max_value=8)


FlightQuerySerializer._declared_fields[
    "from"
] = FlightQuerySerializer._declared_fields.pop("from_")


class FlightAirportDateDefault:
    requires_context = True

    def __call__(self, serializer_field):
        print(type(serializer_field))
        print(serializer_field)


class FlightAirportSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="airport.city.name")
    name = serializers.CharField(source="airport.name")
    iata = serializers.CharField(source="airport.iata")
    date = serializers.DateField(default=FlightAirportDateDefault, allow_null=False)
    time = serializers.TimeField()

    class Meta:
        model = FlightJuncture
        fields = ("city", "name", "iata", "date", "time")


class ActualFlightSerializer(serializers.ModelSerializer):
    flight_id = serializers.IntegerField(source="flight.id")
    flight_code = serializers.CharField(source="flight.code")
    from_ = FlightAirportSerializer(source="flight.departure")
    to = FlightAirportSerializer(source="flight.arrival", required=False)
    cost = serializers.FloatField(source="flight.cost")
    availability = serializers.IntegerField()

    class Meta:
        model = ActualFlight
        fields = ("flight_id", "flight_code", "from", "to", "cost", "availability")


ActualFlightSerializer._declared_fields[
    "from"
] = ActualFlightSerializer._declared_fields.pop("from_")
