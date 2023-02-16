from django.db import models


class FlightJuncture(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()
    airport = models.ForeignKey("airport.Airport", models.DO_NOTHING)

    class Meta:
        db_table = "flight_juncture"

    def __str__(self) -> str:
        return f"Juncture IN {self.airport.iata}, {self.date if self.date else 'everyday'} AT {self.time}"


class Flight(models.Model):
    code = models.CharField(max_length=7)
    cost = models.FloatField()
    departure = models.OneToOneField(
        FlightJuncture, models.DO_NOTHING, related_name="flight_departure"
    )
    arrival = models.OneToOneField(
        FlightJuncture, models.DO_NOTHING, related_name="flight_arrival"
    )

    class Meta:
        db_table = "flight"

    def __str__(self) -> str:
        return f"Flight {self.code} FROM [{self.departure}] TO [{self.arrival}]"
