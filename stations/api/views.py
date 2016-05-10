#from django.shortcuts import render
from django.http import HttpResponse
import json
from depot.models import Station


def get_stations(request):
    stations = []
    for stn in Station.objects.all():
        data = {
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
        stations.append(data)
    output = json.dumps(stations)
    return HttpResponse(output)
