from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Patient
from .models import disease_record
from .forms import add_disease_form
from doctor.models import Doctor, Delete_notifications
from doctor.models import Reservation
from persiantools.jdatetime import JalaliDateTime
import datetime


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    elif not Patient.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    patient = Patient.objects.get(user=request.user)
    deleted_reservations = list(Delete_notifications.objects.filter(patient=patient))

    next_reservations = Reservation.objects.filter(reservation_date__gte=datetime.date.today(),
                                                   patient=patient).order_by('reservation_date', 'start_time')
    next_reservation = None
    current_reservation = None
    for next_reserve in next_reservations:
        if next_reserve.reservation_date == datetime.date.today() and next_reserve.start_time < datetime.datetime.now().time() < next_reserve.end_time:
            current_reservation = next_reserve
            break
        elif next_reserve.reservation_date == datetime.date.today() and next_reserve.start_time > datetime.datetime.now().time():
            next_reservation = next_reserve
            break
        elif next_reserve.reservation_date != datetime.date.today():
            next_reservation = next_reserve
            break

    return render(request, 'patient/profile.html', {'patient': patient, 'deleted_reservations': deleted_reservations,
                                                    'next_reservation': next_reservation,
                                                    'current_reservation': current_reservation})


def disease_records_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    patient = Patient.objects.get(user=request.user)
    disease_records = disease_record.objects.filter(patient=patient)
    records = []
    for record in list(disease_records):
        records.append(record.disease_name)
    if request.method == "GET":
        form = add_disease_form()
    else:
        form = add_disease_form(request.POST)
        if form.is_valid():
            new_record = disease_record.objects.create(patient=patient,
                                                       disease_name=form.cleaned_data['disease_record'])
            new_record.save()
            records.append(new_record.disease_name)
    return redirect('patient:disease_records')


def contact_us_view(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    return render(request, 'patient/contact_us.html')


def remove_record(request, disease):
    disease_record.objects.get(patient__user=request.user, disease_name=disease).delete()
    return redirect('patient:disease_records')


def add_credit(request):
    if not request.user.is_authenticated:
        return redirect('patient:login')
    elif not Patient.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        if 'credit_radio' not in request.POST:
            return render(request, 'patient/add_credit.html', context={'msg': 'یکی از مبالغ را انتخاب کنید',
                                                                       'success': False})
        amount = request.POST['credit_radio'][:-1]
        patient.credit = patient.credit + int(amount)
        patient.save()
        return render(request, 'patient/add_credit.html', context={'msg': 'افزایش اعتبار با موفقیت انجام شد',
                                                                   'success': True})

    return render(request, 'patient/add_credit.html')


def search_doctor(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    if request.method == 'GET':
        if 'doctor_id' not in request.GET:
            return render(request, 'patient/search_doctor.html')
        d_id = request.GET['doctor_id']
        if not Doctor.objects.filter(doctor_id=d_id).count() == 0:
            search_result = Doctor.objects.get(doctor_id=d_id)
            return redirect('patient:reservation', doctor_id=d_id, day=0)

    return render(request, 'patient/search_doctor.html')


def prescriptions(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    patient = Patient.objects.get(user=request.user)
    pres = patient.prescriptioninfo_set.all()
    return render(request, 'patient/prescriptions.html',
                  context={'prescriptions': pres, 'patient': patient})


def reservation(request, doctor_id, day):
    doctor = Doctor.objects.get(pk=doctor_id)
    patient = Patient.objects.get(user=request.user)
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
    elif not Patient.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('users:login')
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

    return render(request, 'patient/reservation.html', {'reservations': reservations, 'date': jalali_time,
                                                        'week_days': week_days, 'reserve_date': future_dates,
                                                        'day': day, 'doctor': doctor, 'patient': patient})


def reserve_time(request, reservation_id, doctor_id):
    patient = Patient.objects.get(user=request.user)
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.patient = patient
    reservation.save()
    return redirect('patient:reservation', doctor_id=doctor_id, day=0)


def reservation_list(request):
    patient = Patient.objects.get(user=request.user)
    reservation_list = list(Reservation.objects.filter(patient=patient).order_by('reservation').order_by('start_time'))
    return render(request, 'patient/reservation_list.html', {'reservation_list': reservation_list})


def delete_notification(request, notification_id):
    Delete_notifications.objects.get(pk=notification_id).delete()
    return redirect('patient:profile')
