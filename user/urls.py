from django.urls import path

from .views import Login, Register, UserBookingsView, UserView

urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("user/", UserView.as_view()),
    path("user/booking/", UserBookingsView.as_view()),
]
