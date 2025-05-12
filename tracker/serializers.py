from rest_framework import serializers
from .models import User, SOSDevice, LocationPing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class SOSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOSDevice
        fields = ['id', 'device_id', 'assigned_user']

class LocationPingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPing
        fields = ['latitude', 'longitude', 'ping_time']
