from django.db import models


class Flight(models.Model):
    code = models.CharField(max_length=7)
    departure = models.OneToOneField(
        "flight_airport.FlightAirport",
        models.DO_NOTHING,
        related_name="flight_departure",
    )
    arrival = models.OneToOneField(
        "flight_airport.FlightAirport",
        models.DO_NOTHING,
        related_name="flight_arrival",
    )
    cost = models.FloatField()
    availability = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = "flight"

    def __str__(self):
        return f"{self.code} {self.departure} -> {self.arrival}"
