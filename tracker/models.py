from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SOSDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    assigned_user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='device')

    def __str__(self):
        return self.device_id

class LocationPing(models.Model):
    device = models.ForeignKey(SOSDevice, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    ping_time = models.DateTimeField()

    class Meta:
        get_latest_by = 'ping_time'
        ordering = ['-ping_time']
