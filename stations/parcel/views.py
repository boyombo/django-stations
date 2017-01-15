from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from parcel.forms import ClientForm, ParcelForm, LoadForm, ArrivalForm,\
    SearchForm, StatusForm
from parcel.models import Parcel
from api.sms import send_message


def format_number(num):
    if len(num) == 11 and num.startswith('0'):
        return '234{}'.format(num[1:])
    elif len(num) == 10:
        return '234{}'.format(num)
    else:
        return num


def register(request):
    if request.method == 'POST':
        cform = ClientForm(request.POST)
        pform = ParcelForm(request.POST)
        if cform.is_valid() and pform.is_valid():
            client = cform.save()
            parcel = pform.save(commit=False)
            parcel.sender = client
            parcel.current_location = parcel.loaded_from
            parcel.status = Parcel.LOADING
            parcel.save()
            msg = 'A parcel has been sent to {} for you from {}. Waybill number is {}'.format(
                parcel.loaded_from.address, parcel.sender.name, parcel.waybill)
            to = format_number(parcel.recipient_phone)
            send_message(to, msg, sender='Parceler')
            messages.success(request, 'Successfully registered parcel')
            return redirect('parcel_register')
    else:
        cform = ClientForm()
        pform = ParcelForm()
    return render(request, 'parcel/register.html',
                  {'cform': cform, 'pform': pform})


def load(request):
    parcels = Parcel.objects.filter(status=Parcel.LOADING)
    if request.method == 'POST':
        form = LoadForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            vehicle = form.cleaned_data['vehicle']
            parcels = form.cleaned_data['parcels']
            print parcels
            parcels.update(
                vehicle=vehicle, loaded_from=location, status=Parcel.TRANSIT)
            vehicle.in_transit = True
            vehicle.location = location
            vehicle.save()
            messages.success(request, 'Successfully loaded parcel')
            return redirect('parcel_load')
    else:
        form = LoadForm()
    return render(
        request, 'parcel/load.html', {'form': form, 'parcels': parcels})


def arrival(request):
    now = timezone.now()
    init_parcels = Parcel.objects.filter(status=Parcel.TRANSIT)
    if request.method == 'POST':
        form = ArrivalForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            vehicle = form.cleaned_data['vehicle']
            parcels = form.cleaned_data['parcels']
            parcels.update(
                status=Parcel.ARRIVED,
                delivered_on=now,
                current_location=location)
            vehicle.location = location
            vehicle.in_transit = False
            vehicle.save()
            # send messages
            for parcel in parcels:
                msg = 'Your parcel with waybill number {} has arrived in {}. Please come with this sms to claim the item'.format(
                    parcel.waybill, parcel.current_location.address)
                to = format_number(parcel.recipient_phone)
                send_message(to, msg, sender='Parceler')

            messages.success(request, 'Successfully processed parcel')
            return redirect('parcel_arrival')
    else:
        form = ArrivalForm()
    return render(
        request,
        'parcel/arrival.html',
        {'form': form, 'parcels': init_parcels})


def arrived_parcels(request):
    parcels = Parcel.objects.filter(status=Parcel.ARRIVED)
    form = SearchForm(request.GET)
    if form.is_valid():
        term = form.cleaned_data['term']
        parcels = parcels.filter(waybill__icontains=term)
    return render(
        request,
        'parcel/arrived.html',
        {'form': form, 'parcels': parcels}
    )


def pickup(request, id):
    parcel = get_object_or_404(Parcel, pk=id)
    if request.method == 'POST':
        parcel.status = Parcel.COLLECTED
        parcel.save()
        msg = 'The parcel you sent to {} with waybill number {} has been collected.'.format(
            parcel.recipient_name, parcel.waybill)
        to = format_number(parcel.client.phone)
        send_message(to, msg, sender='Parceler')
        messages.success(request, 'Parcel collected successfully')
        return redirect('parcel_arrived')
    return render(
        request,
        'parcel/pickup.html',
        {'parcel': parcel}
    )


def status(request):
    parcel = None
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            parcel = form.cleaned_data['waybill']
    else:
        form = StatusForm()
    return render(
        request, 'parcel/search.html', {'parcel': parcel, 'form': form})
