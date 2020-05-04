from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    degrees = models.CharField(max_length=75)


class PrescriptionInfo(models.Model):
    author = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)


class Drug(models.Model):
    drugName = models.CharField(max_length=100, primary_key=True)
    number = models.IntegerField()
    usage = models.CharField(max_length=300, blank=True)
    prescription_id = models.ForeignKey(to=PrescriptionInfo, on_delete=models.CASCADE)



