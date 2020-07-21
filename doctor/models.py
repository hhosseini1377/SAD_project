from django.contrib.auth.models import User
from django.db import models
from patient.models import Patient
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    doctor_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    degrees = models.CharField(max_length=75)


class PrescriptionInfo(models.Model):
    author = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(to=Patient, on_delete=models.CASCADE)


class Drug(models.Model):
    drugName = models.CharField(max_length=100, primary_key=True)
    number = models.IntegerField()
    usage = models.CharField(max_length=300, blank=True)
    prescription_id = models.ForeignKey(to=PrescriptionInfo, on_delete=models.CASCADE)


class Reservation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reservation_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
