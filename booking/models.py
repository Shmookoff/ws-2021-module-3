from django.db import models


class Booking(models.Model):
    code = models.CharField(unique=True, max_length=5)
    cost = models.IntegerField()
    flight_from = models.ForeignKey(
        "flight.Flight",
        models.DO_NOTHING,
        related_name="booking_from",
    )
    flight_back = models.ForeignKey(
        "flight.Flight",
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="booking_back",
    )

    class Meta:
        db_table = "booking"
