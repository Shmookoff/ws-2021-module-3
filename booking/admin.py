from django.contrib import admin

from .models import ActualFlight, Booking, Passenger

admin.site.register([ActualFlight, Booking, Passenger])
