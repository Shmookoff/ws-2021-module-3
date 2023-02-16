import uuid

from django.core.validators import MinLengthValidator
from django.db import models


class User(models.Model):
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(
        unique=True, max_length=11, validators=[MinLengthValidator(11)]
    )
    document_number = models.CharField(
        unique=True, max_length=10, validators=[MinLengthValidator(10)]
    )

    class Meta:
        db_table = "user"


class Token(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, models.CASCADE)
