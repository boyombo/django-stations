from django.shortcuts import render, redirect
from django.contrib import messages

from depot.models import Station, Area, Brand
from depot.forms import StationForm, SearchForm, EntryForm


def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand']
            address = form.cleaned_data['address']
            #area = form.cleaned_data['area']
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            station = Station.objects.create(brand=brand, address=address)
            for name in form.cleaned_data['area']:
                area, _ = Area.objects.get_or_create(name=name)
                station.area.add(area)
            messages.success(request, "Station added successfully")
            return redirect('add_station')
    else:
        form = StationForm()
    return render(request, 'add_station.html', {'form': form})


def station_list(request):
    stations = Station.objects.all()
    form = SearchForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data['name']
        stations = stations.filter(area__name__icontains=name)
    return render(request, 'station_list.html',
                  {'station_list': stations, 'form': form})


def add_entry(request, station_id):
    station = Station.objects.get(pk=station_id)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.station = station
            entry.save()
            messages.success(request, 'Entry updated successfully')
            return redirect('show_list')
    else:
        form = EntryForm()
    return render(request, 'update.html', {'station': station, 'form': form})
