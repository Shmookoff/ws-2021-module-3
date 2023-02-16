from django.contrib.auth.hashers import check_password, make_password
from rest_framework import exceptions, status, views
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializers import GetBookingResponseSerializer
from booking.utils import prepare_booking
from exceptions import UnproccessableEntity

from .models import Token, User
from .serializers import LoginRequest, RegisterRequest, UserResponse


class RegisterView(views.APIView):
    def post(self, request: views.Request):
        serializer = RegisterRequest(data=request.data)
        if not serializer.is_valid():
            raise UnproccessableEntity(serializer.errors)

        data = serializer.validated_data

        serializer.save(password=make_password(data["password"]))

        return views.Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(views.APIView):
    def post(self, request: views.Request):
        serializer = LoginRequest(data=request.data)
        if not serializer.is_valid():
            raise UnproccessableEntity(serializer.errors)

        data = serializer.validated_data

        user = User.objects.filter(phone=data["phone"]).first()

        if not user or not check_password(data["password"], user.password):
            raise exceptions.AuthenticationFailed(
                {"phone": ["phone or password incorrect"]}
            )

        token, _ = Token.objects.get_or_create(user=user)
        return views.Response(data={"token": token.key}, status=status.HTTP_200_OK)


class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: views.Request):
        user = request.user
        serializer = UserResponse(user)
        return views.Response(serializer.data, status.HTTP_200_OK)


class UserBookingsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: views.Request):
        user = request.user
        bookings = Booking.objects.filter(
            passengers__document_number=user.document_number
        )
        bookings_serializer = GetBookingResponseSerializer(
            [prepare_booking(booking) for booking in bookings], many=True
        )
        return views.Response({"items": bookings_serializer.data}, status.HTTP_200_OK)
