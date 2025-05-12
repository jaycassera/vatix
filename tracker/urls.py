from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.list_devices),                      # New: list devices
    path('devices/<int:id>/assign/', views.assign_device),
    path('devices/<int:id>/unassign/', views.unassign_device), # New: unassign device
    path('devices/<int:id>/location/', views.send_location),
    path('users/<int:id>/location/', views.get_user_location),
    path('map/', views.get_map),
]
