from django.urls import path

from . import views

app_name = 'patient'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('disease_records/', views.disease_records_view, name='disease_records'),
    path('contact_us/', views.contact_us_view, name='contact_us')
]