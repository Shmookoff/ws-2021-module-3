from django.urls import path

from .views import FlightSearchView

urlpatterns = [
    path("flight/", FlightSearchView.as_view()),
]
