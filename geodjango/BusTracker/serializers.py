from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from .models import *


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('id', 'name', 'license_number')


class RealTimeBusSerializer(GeoModelSerializer):
    last_updated_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BusRealTime
        geo_field = 'location'
        fields = ('id', 'bus', 'timestamp', 'last_updated_by')



class BusstopSerializer(GeoModelSerializer):
    class Meta:
        model = BusStop
        geo_field = 'location'
        fields = ('id', 'name')


class BusLocationUpdateSerializer(GeoModelSerializer):
    class Meta:
        model = BusRealTime
        geo_field = 'location'
        fields = ('id', 'bus', 'timestamp')


class RouteSerializer(GeoModelSerializer):
    class Meta:
        model = RouteSegment
        geo_field = 'geometry'
        fields = ('id', 'start_stop', 'end_stop', 'distance_km')
        read_only_fields = ('distance_km',)

