from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'patient'
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('disease_records/', views.disease_records_view, name='disease_records'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('remove_record/<disease>/', views.remove_record, name='remove_record'),
    path('add_credit/', views.add_credit, name='add_credit'),
    path('search_doctor/', views.search_doctor, name='search_doctor'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('reservation/<doctor_id>/<day>/', views.reservation, name='reservation'),
    path('reserve_time/<reservation_id>/<doctor_id>/', views.reserve_time, name='reserve_time'),
    path('reservation_list/', views.reservation_list, name="reservation_list"),
    path('delete_notification/<notification_id>/', views.delete_notification, name='delete_notification'),
]
