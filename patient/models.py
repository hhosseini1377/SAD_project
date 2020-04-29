from django.contrib.auth.models import User
from django.db import models
from doctor.models import Doctor
# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    mobile_number = models.IntegerField()
    email = models.EmailField()
    national_id = models.IntegerField(primary_key=True)
    date_of_birth = models.DateField()
    disease_records = models.CharField(max_length=100)
    doctors = models.ManyToManyField(Doctor, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name



