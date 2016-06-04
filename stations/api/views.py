#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from collections import Counter
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
        _state = request.GET.get('state')
        state = drug_models.State.objects.get(name__iexact=_state)
        uuid = form.cleaned_data['uuid']
        try:
            pharmacy = drug_models.Pharmacy.objects.get(uuid=uuid)
        except drug_models.Pharmacy.DoesNotExist:
            pharm = form.save(commit=False)
            pharm.state = state
            pharm.save()
        else:
            pharmacy.name = form.cleaned_data['name']
            pharmacy.phone = form.cleaned_data['phone']
            pharmacy.street = form.cleaned_data['street']
            pharmacy.area = form.cleaned_data['area']
            pharmacy.email = form.cleaned_data['email']
            pharmacy.state = state
            pharmacy.save()
        return HttpResponse("Registered Pharmacy")
    return HttpResponseBadRequest('Unable to register pharmacy')


def add_drug(request):
    form = drug_forms.DrugForm(request.GET)
    #import pdb;pdb.set_trace()
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


def search_drug(request):
    form = drug_forms.SearchForm(request.GET)
    drugs = []
    if form.is_valid():
        item = form.cleaned_data['name'].title()
        uuid = form.cleaned_data['uuid']
        try:
            pharmacy = drug_models.Pharmacy.objects.get(uuid=uuid)
        except drug_models.Pharmacy.DoesNotExist:
            return HttpResponseBadRequest('Please register')
        else:
            drug_models.Search.objects.create(pharmacy=pharmacy, name=item)

        for drug in drug_models.Drug.objects.filter(
                name__icontains=item).order_by('-expiry_date'):
            item = {
                'drug_id': drug.id,
                'name': drug.name,
                'area': drug.pharmacy.area,
                'cost': '{}'.format(drug.cost),
                'expiry': drug.expiry_date.strftime('%Y-%m-%d'),
                'quantity': drug.quantity
            }
            drugs.append(item)
    return HttpResponse(json.dumps(drugs))


def stock_drug(request):
    form = drug_forms.StockForm(request.GET)
    drugs = []
    if form.is_valid():
        uuid = form.cleaned_data['uuid']
        for drug in drug_models.Drug.objects.filter(
                pharmacy__uuid__iexact=uuid):
            item = {
                'drug_id': drug.id,
                'name': drug.name,
                'cost': '{}'.format(drug.cost),
                'expiry': drug.expiry_date.strftime('%Y-%m-%d'),
                'quantity': drug.quantity
            }
            drugs.append(item)
    return HttpResponse(json.dumps(drugs))


def remove_drug(request, id):
    form = drug_forms.StockForm(request.GET)
    if form.is_valid():
        uuid = form.cleaned_data['uuid']
        try:
            drug = drug_models.Drug.objects.get(pk=id, pharmacy__uuid=uuid)
        except drug_models.Drug.DoesNotExist:
            return HttpResponseBadRequest("Wrong drug")
        drug.delete()
        return HttpResponse("Deleted successfully")
    return HttpResponseBadRequest("Error trying to delete drug")


def recent_drugs(request, count):
    drugs = drug_models.Search.objects.values_list('name', flat=True)
    output = []
    for item in Counter(drugs).most_common(int(count)):
        output.append({
            'name': item[0],
            'count': item[1]})
    print output
    return HttpResponse(json.dumps(output))


def wishlist_drug(request):
    form = drug_forms.WishlistForm(request.GET)
    drugs = []
    if form.is_valid():
        pharmacy = form.cleaned_data['uuid']
        searches = drug_models.Search.objects.filter(
            pharmacy=pharmacy).values_list('name', flat=True)
        drugs = list(set(searches))
        print drugs
    return HttpResponse(json.dumps(drugs))


def request_drug(request, drug_id):
    try:
        drug = drug_models.Drug.objects.get(pk=drug_id)
    except drug_models.Drug.DoesNotExist:
        return HttpResponseBadRequest('Wrong drug id')
    form = drug_forms.UUIDForm(request.GET)
    if form.is_valid():
        pharmacy = form.cleaned_data['uuid']
        quantity = form.cleaned_data['quantity']
        drug_models.DrugRequest.objects.create(
            drug=drug, pharmacy=pharmacy, quantity=quantity)
        return HttpResponse('Successfully added request')
    return HttpResponseBadRequest('Error creating request')


def pending_requests(request):
    form = drug_forms.WishlistForm(request.GET)
    output = []
    if form.is_valid():
        pharmacy = form.cleaned_data['uuid']
        requests = drug_models.DrugRequest.objects.filter(
            drug__pharmacy=pharmacy, status=drug_models.DrugRequest.PENDING)
        for item in requests:
            output.append({
                'id': item.id,
                'name': item.drug.name,
                'cost': '{}'.format(item.drug.cost),
                'expiry': item.drug.expiry_date.strftime('%Y-%m-%d'),
                'quantity': item.quantity,
                'date': item.posted_on.strftime('%Y-%m-%d')
            })
    print output
    return HttpResponse(json.dumps(output))


def accept(request, request_id):
    form = drug_forms.WishlistForm(request.GET)
    if form.is_valid():
        pharmacy = form.cleaned_data['uuid']
        try:
            drug_request = drug_models.DrugRequest.objects.get(
                pk=request_id, drug__pharmacy=pharmacy)
        except drug_models.DrugRequest.DoesNotExist:
            return HttpResponseBadRequest('Error accepting request')
        drug_request.status = drug_models.DrugRequest.ACCEPTED
        drug_request.save()
        return HttpResponse("Accepted successfully")
    return HttpResponseBadRequest("Error trying to accept request")


def reject(request, request_id):
    form = drug_forms.WishlistForm(request.GET)
    if form.is_valid():
        pharmacy = form.cleaned_data['uuid']
        try:
            drug_request = drug_models.DrugRequest.objects.get(
                pk=request_id, drug__pharmacy=pharmacy)
        except drug_models.DrugRequest.DoesNotExist:
            return HttpResponseBadRequest('Error rejecting request')
        drug_request.status = drug_models.DrugRequest.CANCELLED
        drug_request.save()
        return HttpResponse("Rejected successfully")
    return HttpResponseBadRequest("Error trying to reject request")
