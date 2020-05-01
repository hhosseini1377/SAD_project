from django.contrib import admin
from .models import Patient
from .models import disease_record
# Register your models here.

admin.site.register(Patient)
admin.site.register(disease_record)