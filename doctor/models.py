from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    degrees = models.CharField(max_length=75)