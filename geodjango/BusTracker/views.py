from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets
from django.contrib.gis.measure import D
from rest_framework.response import Response

from .models import Bus, BusRealTime, BusStop
from .serializers import BusSerializer, RealTimeBusSerializer, BusstopSerializer


# Create your views here.

class BusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class NearbyBusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusRealTime.objects.all()
    serializer_class = RealTimeBusSerializer

    def list(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        radius = request.query_params.get('radius', 5)

        if not(lat and lon):
            return Response({'error': 'Latitude and Longitude are required'}, status=400)
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response({'error': 'Latitude and Longitude are required'}, status=400)

        user_location = Point(lon, lat, srid=4326)
        buses = (
            BusRealTime.objects
            .filter(location__distance_lt=(user_location, D(km=radius)))
            .annotate(distance=Distance('location', user_location))
            .order_by('distance')
        )
        serializer = self.get_serializer(buses, many=True)
        return Response(serializer.data)


class NearbyBusstopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusstopSerializer

    def list(self, request, *args, **kwargs):
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        radius = request.query_params.get('radius', 5)

        if not (lat and lon):
            return Response({'error': 'Latitude and Longitude are required'}, status=400)
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response({'error': 'Latitude and Longitude are required'}, status=400)

        user_location = Point(lon, lat, srid=4326)
        stops = (
            BusStop.objects
            .filter(location__distance_lt=(user_location, D(km=radius)))
            .annotate(distance=Distance('location', user_location))
            .order_by('distance')
        )
        serializer = self.get_serializer(stops, many=True)
        return Response(serializer.data)
