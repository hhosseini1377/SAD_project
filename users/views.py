from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from patient.models import Patient
from pharmacy.models import Pharmacy
from doctor.models import Doctor


def login_view(request):
    if request.user.is_authenticated:
        if Patient.objects.filter(user=request.user).exists():
            return redirect('patient:profile')
        elif Pharmacy.objects.filter(user=request.user).exists():
            return redirect('pharmacy:profile')
        elif Doctor.objects.filter(user=request.user).exists():
            return redirect('doctor:profile')
    logout(request)

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Patient.objects.filter(user=request.user).exists():
                return redirect('patient:profile')
            elif Doctor.objects.filter(user=request.user).exists():
                return redirect('doctor:profile')
            elif Pharmacy.objects.filter(user=request.user).exists():
                pass
        else:
            pass

    else:
        form = AuthenticationForm()
    return render(request, 'users/index.html', {'form': form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    if request.method == 'GET':
        logout(request)
        return redirect('users:login')

