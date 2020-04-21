from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient


def login_view(request):
    if request.user.is_authenticated:
        if Patient.objects.filter(user=request.user).exists():
            return redirect('patient:profile')
    logout(request)
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('patient:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'patient/login.html', {'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('patient:login')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
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


