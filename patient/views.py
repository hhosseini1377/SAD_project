from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Patient.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient/profile.html', {'patient': patient})


def disease_records_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    patient = Patient.objects.get(user=request.user)
    records = patient.disease_records.split("-")
    return render(request, 'patient/disease_records.html', {'records': records})


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    return render(request, 'patient/contact_us.html')


