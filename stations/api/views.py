#from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from depot.models import Station, Brand, Area, State
from depot.forms import EntryForm, APISearchForm, APIStationForm


def add_station(request):
    form = APIStationForm(request.GET)
    if form.is_valid():
        brand_name = form.cleaned_data['brand'].upper()
        address = form.cleaned_data['address']
        state_tag = form.cleaned_data['state'].strip().lower()
        try:
            state = State.objects.get(tag__iexact=state_tag)
        except State.DoesNotExist:
            return HttpResponse('wrong state')

        try:
            brand = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            brand = Brand.objects.create(name=brand_name)

        # Does the station already exist?
        try:
            station = Station.objects.get(
                brand=brand, address=address, state=state)
            return HttpResponse('station already exists')
        except Station.DoesNotExist:
            station = Station.objects.create(
                brand=brand, address=address, state=state)
            for name in form.cleaned_data['area']:
                area, _ = Area.objects.get_or_create(name=name)
                station.area.add(area)
            return HttpResponse('success')
    return HttpResponse('error')


def get_stations(request):
    stations = Station.objects.all()
    form = APISearchForm(request.GET)
    if form.is_valid():
        name = form.cleaned_data['name']
        state = form.cleaned_data['state']
        stations = stations.filter(
            area__name__icontains=name,
            state__tag__iexact=state)
    output = []
    for stn in stations:
        data = {
            'station_id': stn.id,
            'name': stn.brand.name,
            'address': stn.address,
            'num_cars': 'N/A',
            'fuel_price': 'N/A',
            'kegs': 'N/A',
            'time': 'N/A'
            }
        recent = stn.recent
        if recent:
            #kegs = 'Yes' if recent.kegs else 'No'
            data.update({
                'num_cars': recent.get_num_cars_display(),
                'fuel_price': str(recent.fuel_price) or 'N/A',
                'kegs': 'Yes' if recent.kegs else 'No',
                'time': recent.current_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        output.append(data)
    return HttpResponse(json.dumps(output))


@csrf_exempt
def make_entry(request, station_id):
    station = Station.objects.get(pk=station_id)
    #import pdb;pdb.set_trace()
    if request.method == 'GET':
        form = EntryForm(request.GET)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.station = station
            entry.save()
            return HttpResponse('Success')
    return HttpResponse('Error')