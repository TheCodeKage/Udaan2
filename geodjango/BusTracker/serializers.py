from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from .models import *

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('id', 'name', 'license_number')


class RealTimeBusSerializer(GeoModelSerializer):
    class Meta:
        model = BusRealTime
        geo_field = 'location'
        fields = ('id', 'bus', 'timestamp')


class BusstopSerializer(GeoModelSerializer):
    class Meta:
        model = BusStop
        geo_field = 'location'
        fields = ('id', 'name')