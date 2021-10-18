from django.urls import path, include
from rest_framework import routers

from .views import AddressViewset

router = routers.DefaultRouter()
router.register(r'address', AddressViewset)
urlpatterns = [
    path('', include(router.urls)),
]