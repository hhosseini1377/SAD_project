from django.urls import path

from . import views

app_name = 'patient'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('salam/', views.salam, name='salam')
]