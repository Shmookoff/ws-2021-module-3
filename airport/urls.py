from django.urls import path

from .views import AirportSearchView

urlpatterns = [
    path("airport/", AirportSearchView.as_view()),
]
