from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Doctor


# Create your views here.
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'doctor/profile.html', {'doctor': doctor})


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'doctor/contact_us.html')
