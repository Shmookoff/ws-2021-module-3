from django.urls import path

from .views import BookingView

urlpatterns = [
    path("booking/", BookingView.as_view()),
    path("booking/<str:code>/", BookingView.as_view()),
]
