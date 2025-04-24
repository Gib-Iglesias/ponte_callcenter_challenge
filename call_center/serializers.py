from rest_framework import serializers
from .models import CallCenter


class CallCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallCenter
        fields = '__all__'