#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from random import randrange

from depot.models import Station, Area, State
from depot.forms import EntryForm, APISearchForm, APIStationForm
from booking.forms import BookingForm
from insure.models import Device
from insure import forms as insure_forms
from drugshare import forms as drug_forms
from drugshare import models as drug_models


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

        #try:
        #    brand = Brand.objects.get(name=brand_name)
        #except Brand.DoesNotExist:
        #    brand = Brand.objects.create(name=brand_name)

        # Does the station already exist?
        try:
            station = Station.objects.get(
                brand=brand_name, address=address, state=state)
            return HttpResponse('station already exists')
        except Station.DoesNotExist:
            station = Station.objects.create(
                brand=brand_name, address=address, state=state)
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
            'name': stn.brand,
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


def booking(request):
    form = BookingForm(request.GET)
    if form.is_valid():
        obj = form.save(commit=False)
        code = randrange(10002321, 99221025)
        obj.code = code
        obj.save()
        payload = {
            'sender': 'VGCBOOK',
            'to': '234{}'.format(obj.phone[-10:]),
            'msg': "You have been booked into VGC with code: {}".format(code)
        }
        sms_url = 'http://shoutinsms.bayo.webfactional.com/api/sendmsg/'
        requests.get(sms_url, params=payload)
        return HttpResponse('A message has been sent to your visitor.')
    return HttpResponse('Error')


@csrf_exempt
def insure(request):
    form = insure_forms.EntryForm(request.POST, request.FILES)
    # import pdb;pdb.set_trace()
    if form.is_valid():
        obj = form.save(commit=False)
        uuid = request.POST.get('uuid', '')
        if uuid:
            device, _ = Device.objects.get_or_create(uuid=uuid)
            obj.device = device
        obj.save()
        return HttpResponse("Saved building information.")
    return HttpResponseBadRequest("Error")


def register_pharm(request):
    form = drug_forms.PharmacyForm(request.GET)
    #import pdb;pdb.set_trace()
    if form.is_valid():
        pharm = form.save(commit=False)
        _state = request.GET.get('state')
        state = drug_models.State.objects.get(name__iexact=_state)
        pharm.state = state
        pharm.save()
        return HttpResponse("Registered Pharmacy")
    return HttpResponseBadRequest('Unable to register pharmacy')


def add_drug(request):
    form = drug_forms.DrugForm(request.GET)
    if form.is_valid():
        drug = form.save(commit=False)
        uuid = request.GET.get('uuid')
        try:
            pharm = drug_models.Pharmacy.objects.get(uuid=uuid)
        except drug_models.Pharmacy.DoesNotExist:
            return HttpResponseBadRequest("Please register first")
        else:
            drug.pharmacy = pharm
            drug.save()
            return HttpResponse("Drug added")
    return HttpResponseBadRequest('Unable to add the drug')
