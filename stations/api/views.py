#from django.shortcuts import render
from django.http import HttpResponse
import json
from depot.models import Station


def get_stations(request):
    stations = []
    for stn in Station.objects.all():
        data = {'name': stn.brand.name, 'address': stn.address}
        recent = stn.recent
        if recent:
            data.update({
                'num_cars': recent.get_num_cars_display(),
                'fuel_price': str(recent.fuel_price),
                'kegs': recent.kegs,
                'time': recent.current_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        stations.append(data)
    output = json.dumps(stations)
    return HttpResponse(output)
