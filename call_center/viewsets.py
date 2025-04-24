from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import CallCenterSerializer
from .models import CallCenter


class CallCenterViewSet(viewsets.ModelViewSet):
    serializer_class = CallCenterSerializer
    queryset = CallCenter.objects.all()