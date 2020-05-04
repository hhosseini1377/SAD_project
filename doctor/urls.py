from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'doctor'
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('mk_prescription/', views.make_prescription, name='prescription'),
]