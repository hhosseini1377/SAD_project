from django import forms


class add_disease_form(forms.Form):
    disease_record = forms.CharField(max_length=30, label='')