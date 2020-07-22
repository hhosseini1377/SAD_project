from django.contrib import admin
from .models import Doctor, PrescriptionInfo, Drug, Reservation, Delete_notifications

admin.site.register(Doctor)
admin.site.register(PrescriptionInfo)
admin.site.register(Drug)
admin.site.register(Reservation)
admin.site.register(Delete_notifications)