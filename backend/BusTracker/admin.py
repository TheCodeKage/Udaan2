from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import BusRealTime, Bus, BusStop, BusTimes, RouteSegment


@admin.register(BusRealTime)
class BusRealTimeAdmin(GISModelAdmin):
    list_display = ("bus", "timestamp", "location")


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("name", "license_number")


@admin.register(BusStop)
class BusStopAdmin(GISModelAdmin):
    list_display = ("name", "location")


@admin.register(BusTimes)
class BusTimesAdmin(admin.ModelAdmin):
    list_display = ("bus", "stop", "time")

@admin.register(RouteSegment)
class RouteSegmentAdmin(GISModelAdmin):#Fuck you Gopal
    list_display = ("start_stop", "end_stop","geometry","distance_km")
