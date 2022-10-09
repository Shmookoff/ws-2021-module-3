from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Airport
from .serializers import AirportSerializer


class AirportSearchView(APIView):
    serializer_class = AirportSerializer

    def get(self, request):
        query = request.query_params.get("query")
        airports = Airport.objects.all()
        if query:
            airports = airports.filter(
                Q(name__icontains=query)
                | Q(iata=query)
                | Q(city__name__icontains=query)
            )
        serializer = AirportSerializer(airports, many=True, source="items")
        return Response({"items": serializer.data}, status=status.HTTP_200_OK)
