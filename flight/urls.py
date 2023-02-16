from django.urls import path

from .views import FlightQueryView

urlpatterns = [
    path("", FlightQueryView.as_view()),
]
