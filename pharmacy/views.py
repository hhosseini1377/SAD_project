
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse

from .models import Pharmacy, DrugSupply
from doctor.models import PrescriptionInfo
from patient.models import  Patient
from .forms import DrugSupplyForm, PatientIdForm, PrescriptionIdForm
from django.forms import formset_factory
from persiantools.jdatetime import JalaliDateTime


# Create your views here.
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Pharmacy.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    pharmacy = Pharmacy.objects.get(user=request.user)
    return render(request, 'pharmacy/profile.html', context={'pharmacy': pharmacy})


def drug_inventory(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Pharmacy.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    pharmacy = Pharmacy.objects.get(user=request.user)
    drugs = pharmacy.drugsupply_set.all()
    return render(request, 'pharmacy/drug_inventory.html', context={'pharmacy': pharmacy, 'drugs': drugs})


def search_prescriptions(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Pharmacy.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    pharmacy = Pharmacy.objects.get(user=request.user)
    if request.method == 'POST':
        form = PrescriptionIdForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['prescriptionId']
            if not PrescriptionInfo.objects.filter(id=id).exists():
                return render(request, 'pharmacy/search_prescriptions.html', context={
                    'form': form,
                    'msg': "شناسه نسخه اشتباه است",
                })
            prescription = PrescriptionInfo.objects.get(id=id)
            patient = Patient.objects.get(national_id=prescription.patient.national_id)
            return render(request, 'pharmacy/search_prescriptions.html', context={
                'form': form,
                'prescription': prescription,
                'patient': patient,
            })
    else:
        form = PrescriptionIdForm()
    return render(request, 'pharmacy/search_prescriptions.html', context={'form': form})


def add_drug(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Pharmacy.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    pharmacy = Pharmacy.objects.get(user=request.user)
    if request.method == 'POST':
        form = DrugSupplyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if DrugSupply.objects.filter(drugName=data['drugName'], supplier=data['supplier']).exists():
                ds = DrugSupply.objects.get(drugName=data['drugName'], supplier=data['supplier'])
                ds.number += data['drugNo']
                ds.save()
            else:
                ds = DrugSupply(drugName=data['drugName'], supplier=data['supplier'], number=data['drugNo'], pharmacy=pharmacy)
                ds.save()
            return render(request, 'pharmacy/add_drug.html', context={
                'form': DrugSupplyForm(),
                'msg': 'دارو با موفقیت اضافه شد.',
            })
    else:
        form = DrugSupplyForm()
    return render(request, 'pharmacy/add_drug.html', context={'form': form})

