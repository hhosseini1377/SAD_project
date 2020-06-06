from django import forms
from doctor import models as doctor_models
from patient import models as patient_models
from django.forms import widgets


class DrugForm(forms.ModelForm):
    class Meta:
        model = doctor_models.Drug
        fields = ['drugName', 'number', 'usage']
        widgets = {
            'drugName': widgets.TextInput(attrs={'class': 'form-control'}),
            'number': widgets.NumberInput(attrs={'class': 'form-control'}),
            'usage': widgets.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3})}


class reservation_form(forms.Form):
    start_time = forms.TimeField(label='زمان شروع', widget=forms.TimeInput(attrs={'class': 'form_field'}))
    end_time = forms.TimeField(label='زمان پایان', widget=forms.TimeInput(attrs={'class': 'form_field'}))


class PatientForm(forms.Form):
    national_id = forms.IntegerField(min_value=0, max_value=99999999, widget=forms.NumberInput(attrs={'class': 'form-control'}))

