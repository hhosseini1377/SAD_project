from django import forms

class login_form(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField()