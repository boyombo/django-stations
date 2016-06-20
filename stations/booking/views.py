from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from collections import Counter

from booking.forms import ResidentForm, SearchForm, RegisterForm
from booking.models import Resident, Booking, Estate


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']

            username = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd1']
            user = User.objects.create_user(username, email, pwd)
            Estate.objects.create(
                user=user, name=name, phone=phone, address=address)
            return redirect('login')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def resident_list(request):
    estate = request.user.estate
    residents = Resident.objects.filter(estate=estate)
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            resident = form.save(commit=False)
            resident.estate = request.user.estate
            resident.active = False
            resident.save()
            return redirect('resident_list')
    else:
        form = ResidentForm()
    return render(request, 'booking/resident_list.html',
                  {
                      'residents': residents,
                      'sms_credit': 0,
                      'form': form,
                      'estate': estate
                  })


@login_required
def dashboard(request):
    estate = request.user.estate
    bookings = Booking.objects.filter(resident__estate=estate)
    form = SearchForm(request.GET)
    if form.is_valid():
        term = form.cleaned_data['term']
        bookings = bookings.filter(code=term)
    return render(request, 'booking/dashboard.html',
                  {'bookings': bookings, 'form': form})


@login_required
def reports(request):
    reports = Counter(Booking.objects.filter(
        resident__isnull=False).values_list(
        'resident__name', flat=True)).items()
    return render(request, 'booking/reports.html', {'reports': reports})


#def showed_up(request, id):
#    booking = get_object_or_404(Booking, pk=id)
#    booking.visit_time = timezone.now()
#    booking.valid = False
#    booking.save()


def remove(request, id):
    resident = get_object_or_404(Resident, pk=id)
    resident.delete()
    return redirect('dashboard')
