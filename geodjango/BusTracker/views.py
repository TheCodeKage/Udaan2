from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone
from rest_framework import viewsets, permissions
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
import requests
from .models import RouteSegment
from decimal import Decimal

from .models import Bus, BusRealTime, BusStop
from .serializers import BusSerializer, RealTimeBusSerializer, BusstopSerializer, RouteSerializer


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.bus.staff.filter(id=request.user.id).exists()


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


from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.gis.geos import Point

class RealTimeBusViewSet(viewsets.ModelViewSet):
    queryset = BusRealTime.objects.all()
    serializer_class = RealTimeBusSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if 'lat' in data and 'lon' in data:
            instance.location = Point(float(data['lon']), float(data['lat']), srid=4326)
        instance.save()

        data['last_updated_by'] = request.user.id  # or user.pk
        print(data['last_updated_by'])
        data['timestamp'] = timezone.now()  # if auto_now=False
        print(data['timestamp'])

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class RealTimegeometryViewSet(viewsets.ModelViewSet):

    queryset = RouteSegment.objects.all()
    serializer_class = RouteSerializer

    @staticmethod
    def fetch_and_save_osrm_route_with_distance(start_stop, end_stop):
        base_url = "http://router.project-osrm.org/route/v1/driving/"
        start_coord = (start_stop.location.x, start_stop.location.y)
        end_coord = (end_stop.location.x, end_stop.location.y)
        coords = f"{start_coord[0]},{start_coord[1]};{end_coord[0]},{end_coord[1]}"
        url = f"{base_url}{coords}?overview=full&geometries=geojson"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('routes'):
            route = data['routes'][0]
            route_geojson = route['geometry']
            coordinates = route_geojson['coordinates']

            linestring_wkt = "LINESTRING(" + ", ".join(f"{lon} {lat}" for lon, lat in coordinates) + ")"
            route_geom = GEOSGeometry(linestring_wkt)

            distance_meters = route['distance']
            distance_km = Decimal(distance_meters / 1000).quantize(Decimal('0.01'))

            route_segment, created = RouteSegment.objects.update_or_create(
                start_stop=start_stop,
                end_stop=end_stop,
                defaults={
                    'geometry': route_geom,
                    'distance_km': distance_km,
                }
            )
            return route_segment
        else:
            raise Exception("Failed to fetch route from OSRM")
