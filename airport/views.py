from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from .models import Airport
from .serializers import AirportSerializer


class AirportQueryListView(generics.ListAPIView):
    serializer_class = AirportSerializer

    def get_queryset(self):
        queryset = Airport.objects.all()
        query = self.request.query_params.get("query", None)
        if query is not None:
            return queryset.filter(
                Q(iata=query)
                | Q(name__icontains=query)
                | Q(city__name__icontains=query)
            )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AirportSerializer(queryset, many=True)
        return Response({"items": serializer.data})
