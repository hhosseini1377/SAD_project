from django.contrib import admin
from .models import Doctor, PrescriptionInfo, Drug, Reservation
from django_jalali.admin.filters import JDateFieldListFilter

admin.site.register(Doctor)
admin.site.register(PrescriptionInfo)
admin.site.register(Drug)
admin.site.register(Reservation)
