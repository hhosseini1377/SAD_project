from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'pharmacy'
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('search_prescriptions/', views.search_prescriptions, name='search_doctor'),
    path('durg_inventory', views.drug_inventory, name='drug_inventory'),
    path('add_drug', views.add_drug, name='add_drug'),
]