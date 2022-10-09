from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .data import CreateBookingRequestData
from .models import Booking
from .serializers import BookingSerializer, CreateBookingRequestSerializer
from .services import prepare_booking_serialization


class BookingView(APIView):
    serializer_class = CreateBookingRequestSerializer

    def post(self, request):
        req_serializer = CreateBookingRequestSerializer(data=request.data)
        if req_serializer.is_valid():
            req_data = CreateBookingRequestData(**req_serializer.validated_data)
            if req_data.has_enough_seats():
                booking = req_data.create()
                return Response(
                    {"code": booking.code},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"passengers": "Not enough seats"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        return Response(
            req_serializer.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def get(self, request, code):
        try:
            booking = Booking.objects.get(code=code)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")
        serializer = BookingSerializer(prepare_booking_serialization(booking))
        return Response(serializer.data, status=status.HTTP_200_OK)
