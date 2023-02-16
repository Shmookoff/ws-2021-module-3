from django.urls import path

from .views import LoginView, RegisterView, UserBookingsView, UserView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user", UserView.as_view()),
    path("user/booking", UserBookingsView.as_view()),
]
