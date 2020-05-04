from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Doctor, PrescriptionInfo, Drug
from .forms import DrugForm
from django.forms import formset_factory


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


def make_prescription(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    doctor = Doctor.objects.get(user=request.user)
    prescription = PrescriptionInfo(doctor)

    if request.method == 'POST':
        DrugFormSet = formset_factory(DrugForm, extra=1)
        if request.POST['action'] == "اضافه کردن دارو":
            print("adding new drug field")
            formset = DrugFormSet(request.POST)
            if formset.is_valid():
                print(formset.cleaned_data[0])
                formset = DrugFormSet(initial=formset.cleaned_data)
                print("new drug field before render")
            return render(request, 'doctor/prescription.html', context={'formset': formset})
        else:
            formset = DrugFormSet(data=request.POST)
            if formset.is_valid():
                for form in formset.cleaned_data:
                    drugForm = DrugForm(form)
                    drug = drugForm.save(commit=False)
                    drug.prescription_id = prescription
                    drug.save(commit=True)
                prescription.save()
                return render(request, 'doctor/prescription.html', context={'msg': 'نسخه با موفقیت ثبت شد'})
    DrugFormSet = formset_factory(DrugForm)
    formset = DrugFormSet()
    return render(request, 'doctor/prescription.html', context={'formset': formset})
