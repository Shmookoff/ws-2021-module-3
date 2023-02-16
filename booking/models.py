from django.core.validators import MinLengthValidator
from django.db import models


class ActualFlight(models.Model):
    flight = models.ForeignKey(
        "flight.Flight", models.CASCADE, related_name="actual_flights"
    )
    availability = models.IntegerField(default=100)
    date = models.DateField()

    class Meta:
        db_table = "actual_flight"


class Booking(models.Model):
    code = models.CharField(unique=True, max_length=5)
    cost = models.IntegerField()
    flight_from = models.ForeignKey(
        ActualFlight,
        models.CASCADE,
        related_name="booking_from",
    )
    flight_back = models.ForeignKey(
        ActualFlight,
        models.CASCADE,
        blank=True,
        null=True,
        related_name="booking_back",
    )

    class Meta:
        db_table = "booking"


class Passenger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    document_number = models.CharField(
        max_length=10, validators=[MinLengthValidator(10)]
    )
    place_from = models.CharField(max_length=3, null=True, blank=True)
    place_back = models.CharField(max_length=3, null=True, blank=True)
    booking = models.ForeignKey(Booking, models.CASCADE, related_name="passengers")

    class Meta:
        unique_together = ("document_number", "booking")
        db_table = "passenger"
