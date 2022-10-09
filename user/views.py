from booking.models import Booking
from booking.serializers import BookingSerializer
from booking.services import prepare_booking_serialization
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, RegisterSerializer


class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Login(ObtainAuthToken):
    serializer_class = LoginSerializer

    def get_object(self, phone, password):
        try:
            return User.objects.get(phone=phone, password=password)
        except User.DoesNotExist:
            return None

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object(
                serializer.data["phone"], serializer.data["password"]
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(data={"token": token.key}, status=status.HTTP_200_OK)
            return Response(
                data={"phone": ["phone or password incorrect"]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(
            passengers__document_number=user.document_number
        )
        bookings = [prepare_booking_serialization(booking) for booking in bookings]
        serializer = BookingSerializer(bookings, many=True)
        return Response({"items": serializer.data}, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
