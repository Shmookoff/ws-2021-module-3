from django.urls import include, path

urlpatterns = [
    path("", include("user.urls")),
    path("airport", include("airport.urls")),
    path("flight", include("flight.urls")),
    path("booking", include("booking.urls")),
]
