from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(unique=True, max_length=11)
    document_number = models.CharField(
        unique=True, max_length=10, validators=[MinLengthValidator(10)]
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name", "document_number"]

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "user"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
