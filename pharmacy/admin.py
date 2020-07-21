from django.contrib import admin
from .models import Pharmacy
from .models import DrugSupply
# Register your models here.

admin.site.register(Pharmacy)
admin.site.register(DrugSupply)