import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse

from .models import Doctor, PrescriptionInfo, Drug, Reservation, Patient, Delete_notifications
from .forms import DrugForm, reservation_form, PatientForm
from django.forms import formset_factory
from persiantools.jdatetime import JalaliDateTime


# Create your views here.
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    doctor = Doctor.objects.get(user=request.user)
    next_reservations = Reservation.objects.exclude(patient=None).filter(reservation_date__gte=datetime.date.today(),
                                                                         doctor=doctor).order_by('reservation_date',
                                                                                                 'start_time')
    next_reservation = None
    current_reservation = None
    for next_reserve in next_reservations:
        if next_reserve.reservation_date == datetime.date.today() and next_reserve.start_time < datetime.datetime.now().time() < next_reserve.end_time:
            current_reservation = next_reserve
            break
    for next_reserve in next_reservations:
        if next_reserve.reservation_date == datetime.date.today() and next_reserve.start_time > datetime.datetime.now().time():
            next_reservation = next_reserve
            break
        elif next_reserve.reservation_date != datetime.date.today():
            next_reservation = next_reserve
            break
    current_reservation_today = False
    next_reservation_today = False
    if current_reservation is not None:
        if current_reservation.reservation_date == datetime.date.today():
            current_reservation_today = True
    if next_reservation is not None:
        if next_reservation.reservation_date == datetime.date.today():
            next_reservation_today = True
    return render(request, 'doctor/profile.html',
                  {'doctor': doctor, 'current_reservation': current_reservation, 'next_reservation': next_reservation   ,
                   'next_reservation_today': next_reservation_today,
                   'current_reservation_today': current_reservation_today})


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'doctor/contact_us.html')


def patient_prescription(request, patient_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')

    patient = Patient.objects.get(pk=patient_id)
    prescriptions = patient.prescriptioninfo_set.all()
    return render(request, 'doctor/prescriptions.html',
                  context={'prescriptions': prescriptions, 'patient': patient})


def make_prescription(request, patient_pk):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')

    if request.method == 'POST':
        DrugFormSet = formset_factory(DrugForm, extra=1)
        if request.POST['action'] == "اضافه کردن دارو":
            print("adding new drug field")
            formset = DrugFormSet(request.POST)
            if formset.is_valid():
                # print(formset.cleaned_data[0])
                formset = DrugFormSet(initial=formset.cleaned_data)
                # print("new drug field before render")
            return render(request, 'doctor/prescription.html', context={'formset': formset})
        else:
            formset = DrugFormSet(data=request.POST)
            if formset.is_valid():
                doctor = Doctor.objects.get(user=request.user)
                patient = Patient.objects.get(national_id=patient_pk)
                prescription = PrescriptionInfo(author=doctor, patient=patient)
                prescription.save()

                for form_data in formset.cleaned_data:
                    drugForm = DrugForm(data=form_data)
                    drug = drugForm.save(commit=False)
                    drug.prescription_id = prescription
                    drug.save()

                return render(request, 'doctor/prescription.html', context={'msg': 'نسخه با موفقیت ثبت شد'})

    DrugFormSet = formset_factory(DrugForm)
    formset = DrugFormSet()
    return render(request, 'doctor/prescription.html', context={'formset': formset})


def reservation_times(request, day):
    msg = ''
    week_day = {
        0: 'شنبه',
        1: 'یک‌شنبه',
        2: 'دوشنبه',
        3: 'سه‌شنبه',
        4: 'چهارشنبه',
        5: 'پنج‌شنبه',
        6: 'جمعه',
    }
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Doctor.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    doctor = Doctor.objects.get(user=request.user)
    reservation = Reservation.objects.filter(reservation_date=datetime.date.today() + datetime.timedelta(days=int(day)),
                                             doctor=doctor).order_by('start_time')
    reservations = list(reservation)
    reservation_date = datetime.date.today() + datetime.timedelta(days=int(day))
    jalali_time = JalaliDateTime.to_jalali(year=reservation_date.year, month=reservation_date.month,
                                           day=reservation_date.day, hour=0, minute=0, second=0, microsecond=0,
                                           tzinfo=None)
    week_days = []
    for i in range(7):
        week_days.append(week_day.get((i + datetime.date.today().weekday() + 2) % 7))
    future_dates = []
    for i in range(7):
        reserve_date = datetime.date.today() + datetime.timedelta(days=i)
        future_dates.append(
            JalaliDateTime.to_jalali(year=reserve_date.year, month=reserve_date.month, day=reserve_date.day,
                                     hour=0, minute=0, second=0, microsecond=0, tzinfo=None))
    if request.method == 'GET':
        form = reservation_form()
    else:
        form = reservation_form(request.POST)
        if form.is_valid():
            is_valid = True
            if form.cleaned_data['end_time'] < form.cleaned_data['start_time']:
                msg = '.زمان های وارد شده معتبر نمی‌باشند'
                is_valid = False
            for reserve in reservations:
                if form.cleaned_data['end_time'] > reserve.end_time > form.cleaned_data['start_time'] \
                        or form.cleaned_data['end_time'] > reserve.start_time > form.cleaned_data['start_time']:
                    msg = '.تداخل زمانی میان زمان وارد شده با زمان‌های این روز وجود دارد'
                    is_valid = False

            if is_valid:
                new_reserve = Reservation.objects.create(doctor=doctor, start_time=form.cleaned_data['start_time'],
                                                         end_time=form.cleaned_data['end_time'],
                                                         reservation_date=reservation_date)
                reservations.append(new_reserve)
                return redirect('doctor:reservation', day=day)
        else:
            msg = '.فرمت ورودی درست نمی‌باشد'

    return render(request, 'doctor/reservation.html', {'reservations': reservations, 'date': jalali_time,
                                                       'week_days': week_days, 'reserve_date': future_dates,
                                                       'form': form, 'day': day, 'msg': msg})


def delete_reservation(request, reservation_id):
    Reservation.objects.get(pk=reservation_id).delete()
    return redirect('doctor:reservation', day=0)


def reservation_list(request):
    doctor = Doctor.objects.get(user=request.user)
    reservation_list = list(
        Reservation.objects.filter(doctor=doctor).exclude(patient=None).order_by('reservation').order_by('start_time'))
    return render(request, 'doctor/reservation_list.html', {'reservation_list': reservation_list})


def delete_patient_reservation(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    doctor = Doctor.objects.get(user=request.user)
    Delete_notifications.objects.create(patient=reservation.patient, date=reservation.reservation_date, doctor=doctor)
    reservation.patient = None
    reservation.save()
    return redirect('doctor:reservation', day=0)
