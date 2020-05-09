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
            new_record = disease_record.objects.create(patient=patient, disease_name=form.cleaned_data['disease_record'])
            new_record.save()
            records.append(new_record.disease_name)
    return redirect('patient:disease_records')


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    return render(request, 'patient/contact_us.html')


def remove_record(request, disease):
    disease_record.objects.get(patient__user=request.user, disease_name=disease).delete()
    return redirect('patient:disease_records')


def add_credit(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    elif not Patient.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        if 'credit_radio' not in request.POST:
            return render(request, 'patient/add_credit.html', context={'msg': 'یکی از مبالغ را انتخاب کنید',
                                                                       'success': False})
        amount = request.POST['credit_radio'][:-1]
        patient.credit = patient.credit + int(amount)
        patient.save()
        return render(request, 'patient/add_credit.html', context={'msg': 'افزایش اعتبار با موفقیت انجام شد',
                                                                   'success': True})

    return render(request, 'patient/add_credit.html')

