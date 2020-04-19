from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            redirect("patient:salam")
        else:
            redirect("patient:salam")
    else:
        form = AuthenticationForm()
    return render(request, 'patient/login.html', {'form': form})


def salam(request):
    return HttpResponse('s')

