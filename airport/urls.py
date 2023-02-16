from django.urls import path

from .views import AirportQueryListView

urlpatterns = [
    path("", AirportQueryListView.as_view()),
]
