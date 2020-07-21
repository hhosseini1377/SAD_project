
from django import forms
from pharmacy import models as pharmacy_models
from django.forms import widgets


class DrugSupplyForm(forms.Form):
    drugName = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    supplier = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    drugNo = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class PatientIdForm(forms.Form):
    nationalId = forms.IntegerField(min_value=1, max_value=9999999999, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class PrescriptionIdForm(forms.Form):
    prescriptionId = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))