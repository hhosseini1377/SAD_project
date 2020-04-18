from django.db import models

# Create your models here.


class Pharmacy(models.Model):
    name = models.CharField(max_length=50)
    pharmacist = models.CharField(max_length=50)
    drugs = models.CharField(max_length=200)
