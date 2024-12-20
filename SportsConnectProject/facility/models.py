from django.db import models
from django.conf import settings
from datetime import time
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Facilities(models.Model):
    idFacility = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='reservation/facilities/')
    
    def __str__(self):
        return (f"{self.name}")

class Availability(models.Model):
    facilities = models.ForeignKey(Facilities, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time_slot = models.TimeField()
    is_restricted = models.BooleanField(default=False) 
    
    def __str__(self):
        return (f"{self.facilities.name} - [{self.date} - {self.time_slot}]")

    # para una facility, en una date determinada, cada time_slot solo se puede asignar una vez
    class Meta:
        unique_together = ('facilities', 'date', 'time_slot')

    def generate_time_slots(self):
        # Generate time slots from 5am to 5pm
        slots = []
        for hour in range(6, 21):
            slots.append(time(hour=hour, minute=0))
        return slots
