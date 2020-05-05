from django import forms
from doctor import models
from django.forms import widgets

class DrugForm(forms.ModelForm):
    class Meta:
        model = models.Drug
        fields = ['drugName', 'number', 'usage']
        widgets = {
            'drugName': widgets.TextInput(attrs={'class': 'form-control'}),
            'number': widgets.NumberInput(attrs={'class': 'form-control'}),
            'usage': widgets.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3})}


