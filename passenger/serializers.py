from rest_framework import serializers

from .models import Passenger


class PassengerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "birth_date", "document_number")


class PassengerSerializer(serializers.ModelSerializer):
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
