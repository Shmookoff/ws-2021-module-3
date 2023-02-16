from django.contrib import admin

from .models import Flight, FlightJuncture

# Register your models here.
admin.site.register((Flight, FlightJuncture))
