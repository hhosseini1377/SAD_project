from django.contrib import admin
from .models import Doctor, PrescriptionInfo, Drug

# Register your models here.

admin.site.register(Doctor)
admin.site.register(PrescriptionInfo)
admin.site.register(Drug)
