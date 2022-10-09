from rest_framework import serializers


class SeatSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField()
    place = serializers.CharField()


class BookingSeatSerializer(serializers.Serializer):
    occupied_from = SeatSerializer(many=True)
    occupied_back = SeatSerializer(many=True, allow_empty=True)


class BookingSeatChoiceRequestSerializer(serializers.Serializer):
    passenger = serializers.IntegerField()
    seat = serializers.CharField()
    type = serializers.ChoiceField(choices=("from", "back"))
