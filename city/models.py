from django.db import models


class City(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = "city"

    def __str__(self) -> str:
        return f"City {self.name}"
