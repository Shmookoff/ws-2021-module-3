from django.db import models


class Airport(models.Model):
    name = models.CharField(unique=True, max_length=100)
    iata = models.CharField(unique=True, max_length=3)
    city = models.ForeignKey("city.City", models.DO_NOTHING)

    class Meta:
        db_table = "airport"

    def __str__(self):
        return self.iata
