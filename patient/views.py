from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Patient
from .models import disease_record
from .forms import add_disease_form


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
        return redirect('user:login')
    patient = Patient.objects.get(user=request.user)
    disease_records = disease_record.objects.filter(patient=patient)
    records = []
    for record in list(disease_records):
        records.append(record.disease_name)
    if request.method == "GET":
        form = add_disease_form()
    else:
        form = add_disease_form(request.POST)
        if form.is_valid():
            disease_record.objects.create(patient=patient, disease_name=form.cleaned_data['disease_record']).save()
    return render(request, 'patient/disease_records.html', {'records': records, 'form': form})


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    return render(request, 'patient/contact_us.html')


def remove_record(request, disease):
    disease_record.objects.get(patient__user=request.user, disease_name=disease).delete()
    return redirect('patient:disease_records')

