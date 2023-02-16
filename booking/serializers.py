from rest_framework import serializers

from flight.serializers import ActualFlightSerializer

from .models import Passenger


class CreateBookingRequestFlightSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()


class CreateBookingRequestPassengerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birth_date = serializers.DateField()
    document_number = serializers.CharField(min_length=10, max_length=10)


class CreateBookingRequestSerializer(serializers.Serializer):
    flight_from = CreateBookingRequestFlightSerializer()
    flight_back = CreateBookingRequestFlightSerializer(required=False)
    passengers = CreateBookingRequestPassengerSerializer(many=True)


class GetBookingResponsePassengerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk")

    class Meta:
        model = Passenger
        fields = (
            "id",
            "first_name",
            "last_name",
            "birth_date",
            "document_number",
            "place_from",
            "place_back",
        )


class GetBookingResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    cost = serializers.FloatField()
    flights = ActualFlightSerializer(many=True)
    passengers = GetBookingResponsePassengerSerializer(many=True)


class PatchSeatRequestSerializer(serializers.Serializer):
    passenger = serializers.IntegerField()
    seat = serializers.CharField()
    type = serializers.ChoiceField([("from", "from"), ("back", "back")])
