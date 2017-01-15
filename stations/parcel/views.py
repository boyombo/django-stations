from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from parcel.forms import ClientForm, ParcelForm, LoadForm, ArrivalForm,\
    SearchForm, StatusForm
from parcel.models import Parcel


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
