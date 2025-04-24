from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import CallCenter
from .serializers import CallCenterSerializer


# CallCenter CRUD
class ListAereoView(generics.ListAPIView):
    allowed_methods = ['GET']
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

class ListIdAereoView(generics.RetrieveAPIView):
    allowed_methods = ['GET']
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

class CreateAereoView(generics.CreateAPIView):
    allowed_methods = ['POST']
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

class EditAereoView(generics.UpdateAPIView):
    allowed_methods = ['PUT']
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

class DeleteAereoView(generics.DestroyAPIView):
    allowed_methods = ['DELETE']
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer
