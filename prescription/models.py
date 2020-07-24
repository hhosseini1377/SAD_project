from django.db import models
from doctor.models import Doctor
from patient.models import Patient
# Create your models here.


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(Patient)
    insurance = models.ForeignKey(Insurance)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    drugs = models.CharField(max_length=100)