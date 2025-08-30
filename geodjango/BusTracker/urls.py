from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('bus', BusViewSet)
router.register('rtbus', NearbyBusViewSet, basename='rtbus')
router.register('busstop', NearbyBusstopViewSet, basename='busstop')

urlpatterns = [
    path('', include(router.urls)),
]