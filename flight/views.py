from django.db.models import Q
from rest_framework import status, views
from rest_framework.response import Response

from booking.models import ActualFlight

from .models import Flight
from .serializers import ActualFlightSerializer, FlightQuerySerializer


class FlightQueryView(views.APIView):
    @staticmethod
    def get_flights(filters: dict):
        flights = Flight.objects.filter(
            Q(departure__date=filters["date"]) | Q(departure__date__isnull=True),
            departure__airport__iata=filters["from"],
            arrival__airport__iata=filters["to"],
        )
        actual_flights = []
        for flight in flights:
            actual_flight, _ = ActualFlight.objects.get_or_create(
                flight=flight, date=filters["date"]
            )
            if actual_flight.availability >= filters["passengers"]:
                actual_flights.append(actual_flight)
        return ActualFlightSerializer(actual_flights, many=True).data

    @classmethod
    def search_flights(cls, filters: dict):
        flights = cls.get_flights(filters)
        for flight in flights:
            flight["to"]["date"] = filters["date"]
            flight["from"]["date"] = filters["date"]
        return flights

    def get(self, request: views.Request):
        q_serializer = FlightQuerySerializer(data=request.query_params)
        if not q_serializer.is_valid():
            return Response(
                q_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        q = q_serializer.data
        data = {
            "flights_to": self.search_flights(q | {"date": q["date1"]}),
            "flights_back": self.search_flights(
                q | {"to": q["from"], "from": q["to"], "date": q["date2"]}
            )
            if q["date2"]
            else [],
        }

        return Response(data, status=status.HTTP_200_OK)
