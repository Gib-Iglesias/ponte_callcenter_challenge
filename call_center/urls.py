from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import CallCenterViewSet


router = DefaultRouter()
router.register(r'call-center', CallCenterViewSet)

urlpatterns = []

urlpatterns += router.urls
