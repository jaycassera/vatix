from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, SOSDevice, LocationPing
from .serializers import UserSerializer, LocationPingSerializer, SOSDeviceSerializer


@api_view(['POST'])
def assign_device(request, id):
    try:
        device = SOSDevice.objects.get(pk=id)
    except SOSDevice.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

    user_id = request.data.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # Unassign device from any current user
    if device.assigned_user:
        device.assigned_user.device = None

    # BONUS 3: Validate that users can’t have multiple active devices
    # Unassign any existing device from this user
    existing_device = getattr(user, 'device', None)
    if existing_device:
        existing_device.assigned_user = None
        existing_device.save()

    device.assigned_user = user
    device.save()

    return Response({'message': 'Device assigned'}, status=200)

@api_view(['POST'])
def send_location(request, id):
    try:
        device = SOSDevice.objects.get(pk=id)
    except SOSDevice.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

    if not device.assigned_user:
        return Response({'error': 'Device not assigned'}, status=400)

    serializer = LocationPingSerializer(data=request.data)
    if serializer.is_valid():
        LocationPing.objects.create(
            device=device,
            **serializer.validated_data
        )
        return Response({'message': 'Location recorded'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_user_location(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    device = getattr(user, 'device', None)
    if not device:
        return Response({'error': 'User has no assigned device'}, status=404)

    last_ping = device.locations.first()
    if not last_ping:
        return Response({'error': 'No location data available'}, status=404)

    return Response({
        'latitude': last_ping.latitude,
        'longitude': last_ping.longitude,
        'timestamp': last_ping.ping_time
    })

# BONUS 4: Add simple query param filter to /map/ for device type or user ID
@api_view(['GET'])
def get_map(request):
    user_id = request.query_params.get('user_id')
    device_id = request.query_params.get('device_id')

    devices = SOSDevice.objects.filter(assigned_user__isnull=False)

    if user_id:
        devices = devices.filter(assigned_user__id=user_id)
    if device_id:
        devices = devices.filter(device_id=device_id)

    result = []
    for device in devices:
        last_ping = device.locations.first()
        if last_ping:
            result.append({
                'user': {
                    'id': device.assigned_user.id,
                    'name': device.assigned_user.name,
                },
                'device_id': device.device_id,
                'latitude': last_ping.latitude,
                'longitude': last_ping.longitude,
                'timestamp': last_ping.ping_time
            })
    return Response(result)

# BONUS 1: Add GET /devices/ to see all devices and their assignment status
@api_view(['GET'])
def list_devices(request):
    devices = SOSDevice.objects.all()
    data = [
        {
            'device_id': device.device_id,
            'assigned_user': {
                'id': device.assigned_user.id,
                'name': device.assigned_user.name
            } if device.assigned_user else None
        }
        for device in devices
    ]
    return Response(data)

# BONUS 2: Add POST /devices/<id>/unassign/
@api_view(['POST'])
def unassign_device(request, id):
    try:
        device = SOSDevice.objects.get(pk=id)
    except SOSDevice.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

    device.assigned_user = None
    device.save()
    return Response({'message': 'Device unassigned'}, status=200)
