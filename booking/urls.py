from django.urls import path

from .views import BookingView, SeatView

urlpatterns = [
    path("", BookingView.as_view()),
    path("/<str:code>", BookingView.as_view()),
    path("/<str:code>/seat", SeatView.as_view()),
]
