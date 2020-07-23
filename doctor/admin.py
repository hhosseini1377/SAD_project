from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(PrescriptionInfo)
admin.site.register(Drug)
admin.site.register(Reservation)
admin.site.register(DoctorProfession)
admin.site.register(Delete_notifications)