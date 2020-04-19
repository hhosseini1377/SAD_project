from django.contrib.auth.models import User
from django.db import models
from insurance.models import Insurance
from doctor.models import Doctor
# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    national_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    disease_records = models.CharField(max_length=100)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, blank=True, null=True)
    doctors = models.ManyToManyField(Doctor, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name



