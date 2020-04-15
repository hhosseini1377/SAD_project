from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.IntegerField(primary_key=True)
    date_of_birth = models.CharField(max_length=15)
    disease_records = models.CharField(max_length=100)


