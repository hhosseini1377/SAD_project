from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pharmacist = models.CharField(max_length=50)


class DrugSupply(models.Model):
    drugName = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    number = models.IntegerField()
    pharmacy = models.ForeignKey(to=Pharmacy, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("drugName", "supplier"), )
