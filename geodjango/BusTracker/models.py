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
    license_number = models.CharField(max_length=100)
    stops = models.ManyToManyField(BusStop, through='BusTimes', related_name='buses')
    staff = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class BusRealTime(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    location = models.PointField(geography=True, srid=4326)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bus.name
