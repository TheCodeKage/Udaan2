from django.contrib.auth.models import User
from django.contrib.gis.db import models

# Create your models here.
class BusStop(models.Model):
    location = models.PointField(geography=True, srid=4326)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusTimes(models.Model):
    stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='times')
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE, related_name='times')
    time = models.TimeField()

    def __str__(self):
        return self.stop.name


class Bus(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100, unique=True)
    stops = models.ManyToManyField(BusStop, through='BusTimes', related_name='buses')
    staff = models.ManyToManyField(User, related_name='buses')

    def __str__(self):
        return self.name


class BusRealTime(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    location = models.PointField(geography=True, srid=4326)
    timestamp = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.bus.name

class RouteSegment(models.Model):
    start_stop = models.ForeignKey(BusStop, related_name='route_start_segments', on_delete=models.CASCADE)
    end_stop = models.ForeignKey(BusStop, related_name='route_end_segments', on_delete=models.CASCADE)
    geometry = models.LineStringField(srid=4326, blank=True, null=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True )

    def __str__(self):
        return f"Route from {self.start_stop.name} to {self.end_stop.name}"

'''class Route(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    start_stop = models.ManyToManyField(BusStop, on_delete=models.CASCADE, related_name='routes')
    geometry = models.LineStringField(srid=4326)


class BusRoute(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

'''
