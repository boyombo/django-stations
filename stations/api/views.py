#from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from depot.models import Station
from depot.forms import EntryForm, APISearchForm


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
