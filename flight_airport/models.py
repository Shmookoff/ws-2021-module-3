import datetime

from django.db import models


class FlightAirport(models.Model):
    airport = models.ForeignKey("airport.Airport", models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()

    class Meta:
        db_table = "flight_airport"

    def __str__(self):
        return f"{self.airport} {self.date} {self.time}"
