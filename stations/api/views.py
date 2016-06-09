#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
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
    form = drug_forms.RegisterForm(request.GET)
    #import pdb;pdb.set_trace()
    if form.is_valid():
        uuid = form.cleaned_data['uuid']
        try:
            drug_models.Device.objects.get(uuid=uuid)
        except drug_models.Device.DoesNotExist:
            pharmacy = drug_models.Pharmacy.objects.create(
                name=form.cleaned_data['pharmacy'],
                pharmacist=form.cleaned_data['pharmacist'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'])
            device = drug_models.Device.objects.create(
                pharmacy=pharmacy, uuid=uuid)
            out = {
                'name': pharmacy.name,
                'pharmacist': pharmacy.pharmacist,
                'phone': pharmacy.phone,
                'email': pharmacy.email,
                'id': pharmacy.id,
                'device_id': device.id,
                'outlets': []
            }
            return HttpResponse(json.dumps(out))
    return HttpResponseBadRequest('Unable to register')


def get_profile(request):
    form = drug_forms.DeviceForm(request.GET)
    if form.is_valid():
        device = form.cleaned_data['uuid']
        if not device.active:
            return HttpResponseBadRequest('Inactive device')
        out = {
            'name': device.pharmacy.name,
            'pharmacist': device.pharmacy.pharmacist,
            'phone': device.pharmacy.phone,
            'email': device.pharmacy.email,
            'id': device.pharmacy.id,
            'device_id': device.id
        }
        outlets = []
        for outlet in drug_models.Outlet.objects.filter(
                pharmacy=device.pharmacy, active=True):
            outlets.append({
                'id': outlet.id,
                'phone': outlet.phone,
                'address': outlet.address,
                'state': outlet.state.name
            })
        out['outlets'] = outlets
        print out
        return HttpResponse(json.dumps(out))
    return HttpResponseBadRequest("Error")


def delete_outlet(request, id):
    outlet = get_object_or_404(drug_models.Outlet, pk=id)
    outlet.active = False
    outlet.save()
    return HttpResponse('Successfully deleted outlet')


def update_pharm(request, id):
    pharmacy = get_object_or_404(drug_models.Pharmacy, id=id)
    form = drug_forms.PharmacyForm(request.GET, instance=pharmacy)
    #import pdb;pdb.set_trace()
    if form.is_valid():
        form.save()
        #pharmacy.name = form.cleaned_data['name']
        #pharmacy.phamacist = form.cleaned_data['pharmacist']
        #pharmacy.phone = form.cleaned_data['phone']
        #pharmacy.email = form.cleaned_data['email']
        #pharmacy.save()
        return HttpResponse("Saved Pharmacy")
    return HttpResponseBadRequest('Unable to save Pharmacy')


def add_outlet(request, id):
    pharmacy = get_object_or_404(drug_models.Pharmacy, id=id)
    #import pdb;pdb.set_trace()
    form = drug_forms.OutletForm(request.GET)
    if form.is_valid():
        _state = request.GET.get('state')
        state = drug_models.State.objects.get(name__iexact=_state)
        outlet = form.save(commit=False)
        outlet.pharmacy = pharmacy
        outlet.state = state
        outlet.active = True
        outlet.save()
        return HttpResponse("Saved Outlet")
    return HttpResponseBadRequest('Unable to save Outlet')


def list_generic_drugs(request):
    output = []
    drugs = drug_models.Drug.objects.distinct('name')
    for item in drugs:
        output.append({
            'id': item.id,
            'name': item.name
        })
    print output
    return HttpResponse(json.dumps(output))


def add_drug(request):
    form = drug_forms.DrugForm(request.GET)
    #import pdb;pdb.set_trace()
    if form.is_valid():
        form.save()
        return HttpResponse("Drug added")
    return HttpResponseBadRequest('Unable to add the drug')


def search_drug(request, id):
    device = get_object_or_404(drug_models.Device, pk=id)
    form = drug_forms.SearchForm(request.GET)
    drugs = []
    if form.is_valid():
        item = form.cleaned_data['name'].title()
        drug_models.Search.objects.create(pharmacy=device.pharmacy, name=item)

        for drug in drug_models.Drug.objects.filter(
                Q(name__icontains=item) | Q(brand_name__icontains=item)
                ).order_by('-expiry_date'):
            item = {
                'id': drug.id,
                'name': drug.name,
                'brand': drug.brand_name,
                'state': drug.outlet.state.name,
                'cost': '{}'.format(drug.cost),
                'expiry': drug.expiry_date.strftime('%Y-%m-%d'),
                'quantity': drug.quantity,
                'packsize': drug.pack_size
            }
            drugs.append(item)
    return HttpResponse(json.dumps(drugs))


def stock_drug(request, id):
    pharmacy = get_object_or_404(drug_models.Pharmacy, pk=id)
    drugs = []
    for drug in drug_models.Drug.objects.filter(
            outlet__pharmacy=pharmacy):
        item = {
            'id': drug.id,
            'name': drug.name,
            'cost': '{}'.format(drug.cost),
            'packsize': drug.pack_size,
            'expiry': drug.expiry_date.strftime('%Y-%m-%d'),
            'quantity': drug.quantity,
            'address': drug.outlet.address
        }

        drugs.append(item)
    return HttpResponse(json.dumps(drugs))


def remove_drug(request, id):
    drug = get_object_or_404(drug_models.Drug, pk=id)
    drug.delete()
    return HttpResponse("Deleted successfully")


def edit_drug(request, id):
    drug = get_object_or_404(drug_models.Drug, pk=id)
    form = drug_forms.QtyForm(request.GET)
    if form.is_valid():
        drug.quantity = form.cleaned_data['quantity']
        drug.save()
        return HttpResponse("Updated successfully")
    return HttpResponseBadRequest("Error trying to update drug")


def recent_drugs(request, count):
    drugs = drug_models.Search.objects.values_list('name', flat=True)
    output = []
    for item in Counter(drugs).most_common(int(count)):
        output.append({
            'name': item[0],
            'count': item[1]})
    print output
    return HttpResponse(json.dumps(output))


def wishlist_drug(request, pharm_id):
    pharmacy = get_object_or_404(drug_models.Pharmacy, pk=pharm_id)
    print "pharmacy %s" % pharmacy
    drugs = []
    for item in drug_models.DrugRequest.objects.filter(
            outlet__pharmacy=pharmacy,
            status=drug_models.DrugRequest.PENDING):
        drugs.append({
            'name': item.drug.name,
            'brand': item.drug.brand_name,
            'outlet': item.outlet.address,
            'quantity': item.quantity,
            'cost': "{}".format(item.drug.cost),
            'packsize': item.drug.pack_size,
            'expiry': item.drug.expiry_date.strftime('%Y-%m-%d')
        })
    return HttpResponse(json.dumps(drugs))


def request_drug(request, drug_id):
    drug = get_object_or_404(drug_models.Drug, pk=drug_id)
    form = drug_forms.DrugRequestForm(request.GET)
    if form.is_valid():
        outlet = form.cleaned_data['outlet']
        quantity = form.cleaned_data['quantity']
        drug_models.DrugRequest.objects.create(
            drug=drug, outlet=outlet, quantity=quantity)
        return HttpResponse('Successfully added request')
    return HttpResponseBadRequest('Error creating request')


def pending_requests(request, pharm_id):
    pharmacy = get_object_or_404(drug_models.Pharmacy, pk=pharm_id)
    print "pharmacy %s" % pharmacy
    output = []
    for item in drug_models.DrugRequest.objects.filter(
            drug__outlet__pharmacy=pharmacy,
            status=drug_models.DrugRequest.PENDING):
        output.append({
            'id': item.id,
            'name': item.drug.name,
            'cost': '{}'.format(item.drug.cost),
            'expiry': item.drug.expiry_date.strftime('%Y-%m-%d'),
            'quantity': item.quantity,
            'date': item.posted_on.strftime('%Y-%m-%d'),
            'state': item.drug.outlet.state.name
        })
    print output
    return HttpResponse(json.dumps(output))


def accept(request, request_id):
    drug_request = get_object_or_404(drug_models.DrugRequest, pk=request_id)
    drug_request.status = drug_models.DrugRequest.ACCEPTED
    drug_request.save()
    return HttpResponse("Accepted successfully")


def reject(request, request_id):
    drug_request = get_object_or_404(drug_models.DrugRequest, pk=request_id)
    drug_request.status = drug_models.DrugRequest.CANCELLED
    drug_request.save()
    return HttpResponse("Rejected successfully")
