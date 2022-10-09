from django.urls import path

from .views import BookingSeatView

urlpatterns = [
    path("booking/<str:code>/seat", BookingSeatView.as_view()),
]
