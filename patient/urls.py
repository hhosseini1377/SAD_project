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
    path('search_doctor/', views.search_doctor, name='search_doctor')
]