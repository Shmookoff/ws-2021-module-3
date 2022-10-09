from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flight
from .serializers import FlightQuerySerializer, FlightSerializer


class FlightSearchView(APIView):
    def search_flights(self, from_, to, date, passengers):
        if date:
            flights = Flight.objects.filter(
                Q(departure__date=date) | Q(departure__date__isnull=True),
                departure__airport__iata=from_,
                arrival__airport__iata=to,
                availability__gte=passengers,
            )
            return FlightSerializer(flights, many=True).data
        return []

    def get(self, request):
        q_serializer = FlightQuerySerializer(data=request.query_params)
        if q_serializer.is_valid():
            q_data = q_serializer.validated_data
            print(q_data)
            flights_to = self.search_flights(
                q_data["from"],
                q_data["to"],
                q_data["date1"],
                q_data["passengers"],
            )
            flights_back = self.search_flights(
                q_data["to"],
                q_data["from"],
                q_data["date2"],
                q_data["passengers"],
            )
            return Response(
                {"flights_to": flights_to, "flights_back": flights_back},
                status=status.HTTP_200_OK,
            )
        return Response(
            q_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
