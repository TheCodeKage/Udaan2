from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

router = DefaultRouter()
router.register('bus', BusViewSet, basename='bus')
router.register('rtbus', NearbyBusViewSet, basename='rtbus')
router.register('busstop', NearbyBusstopViewSet, basename='busstop')
router.register('update', RealTimeBusViewSet, basename='update')
router.register('geometry',RealTimegeometryViewSet, basename='geometry')
urlpatterns = [
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
#urlpatterns = format_suffix_patterns(urlpatterns)