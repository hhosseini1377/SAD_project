from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'doctor'
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('mk_prescription/<patient_pk>/', views.make_prescription, name='make_prescription'),
    path('prescriptions/', views.patient_prescription, name='prescriptions'),
    path('reservation/<day>/', views.reservation_times, name='reservation'),
    path('remove_reservation/<reservation_id>/', views.delete_reservation, name='remove_reservation'),

]