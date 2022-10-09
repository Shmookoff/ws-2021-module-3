from django.core.validators import MinLengthValidator
from django.db import models


class Passenger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    document_number = models.CharField(
        unique=True, max_length=10, validators=[MinLengthValidator(10)]
    )
    booking = models.ForeignKey(
        "booking.Booking", models.DO_NOTHING, related_name="passengers"
    )
    place_from = models.CharField(max_length=3, null=True, blank=True)
    place_back = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        db_table = "passenger"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
