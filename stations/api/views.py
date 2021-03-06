#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
import requests
from collections import Counter
from random import randrange
from datetime import date

from depot.models import Station, Area, State
from depot.forms import EntryForm, APISearchForm, APIStationForm
from booking.forms import BookingForm
from booking import models as booking_models
from insure.models import Device
from insure import forms as insure_forms
from drugshare import forms as drug_forms
from drugshare import models as drug_models
from api.sms import send_message


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


def booking(request, resident_id):
    resident = get_object_or_404(booking_models.Resident, pk=resident_id)
    estate = resident.estate
    form = BookingForm(request.GET)
    #import pdb;pdb.set_trace()
    if form.is_valid():
        obj = form.save(commit=False)
        code = randrange(10002321, 99221025)
        obj.code = code
        obj.resident = resident
        obj.save()
        msg = "You have been booked by {resident.name} into\
                {resident.estate.name} with code: {code}".format(
            resident=resident, code=code)
        phone = '234{}'.format(obj.phone[-10:])
        #payload = {
        #    'sender': 'V LOGIN',
        #    'to': '234{}'.format(obj.phone[-10:]),
        #    'msg': msg
        #}
        send_message(phone, msg)
        #sms_url = 'http://shoutinsms.bayo.webfactional.com/api/sendmsg/'
        #requests.get(sms_url, params=payload)
        booking_models.SentMessage.objects.create(resident=resident)
        estate.balance -= 1
        estate.save()
        return HttpResponse('A message has been sent to your visitor.')
    return HttpResponseBadRequest('An error occured. Please try again')


def book_profile(request):
    uuid = request.GET.get('uuid')
    device = get_object_or_404(
        booking_models.Device, uuid=uuid, resident__isnull=False)
    out = {
        'device_id': device.id,
        'resident_id': device.resident.id,
        'estate_id': device.resident.estate.id
    }
    print out
    return HttpResponse(json.dumps(out))


def book_phone(request):
    phone = request.GET.get('phone')
    uuid = request.GET.get('uuid')

    try:
        booking_models.Resident.objects.get(phone=phone)
    except booking_models.Resident.DoesNotExist:
        return HttpResponseBadRequest('Sorry you have not been registered')
    else:
        try:
            booking_models.Token.objects.get(msisdn=phone)
        except booking_models.Token.DoesNotExist:
            code = randrange(100321, 992125)
            booking_models.Token.objects.create(
                code=code, msisdn=phone, uuid=uuid)
            #payload = {
            #    'sender': 'V LOGIN',
            #    'to': phone,
            #    'msg': 'This is your verification code: {}'.format(code)
            #}
            msg = 'This is your verification code: {}'.format(code)
            send_message(phone, msg)
            #sms_url = 'http://shoutinsms.bayo.webfactional.com/api/sendmsg/'
            #requests.get(sms_url, params=payload)
            return HttpResponse('The verification code has been sent to you.')
        else:
            return HttpResponseBadRequest(
                'A verification code has already been sent')
    return HttpResponseBadRequest(
        'An unfortunate error occured, please contact the admin')


def book_code(request):
    code = request.GET.get('code')
    uuid = request.GET.get('uuid')
    try:
        token = booking_models.Token.objects.get(code=code, uuid=uuid)
    except booking_models.Token.DoesNotExist:
        return HttpResponseBadRequest('The code you sent is invalid')
    else:
        resident = booking_models.Resident.objects.get(phone=token.msisdn)
        resident.active = True
        resident.save()
        device = booking_models.Device.objects.create(
            uuid=uuid, resident=resident)
        out = {
            'device_id': device.id,
            'resident_id': device.resident.id,
            'estate_id': device.resident.estate.id
        }
        return HttpResponse(json.dumps(out))
    return HttpResponseBadRequest('Error, please contact the admin')


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


def add_device(request):
    form = drug_forms.TokenForm(request.GET)
    if form.is_valid():
        code = form.cleaned_data['code']
        uuid = form.cleaned_data['uuid']
        try:
            token = drug_models.Token.objects.get(
                code=code, when=date.today())
        except drug_models.Token.DoesNotExist:
            return HttpResponseBadRequest('Token not valid')
        else:
            pharmacy = token.pharmacy
            device = drug_models.Device.objects.create(
                pharmacy=pharmacy, uuid=uuid)
            out = {

                'name': pharmacy.name,
                'pharmacist': pharmacy.pharmacist,
                'phone': pharmacy.phone,
                'email': pharmacy.email,
                'id': pharmacy.id,
                'device_id': device.id,
            }
            outlets = []
            for outlet in drug_models.Outlet.objects.filter(
                    pharmacy=pharmacy, active=True):
                outlets.append({
                    'id': outlet.id,
                    'phone': outlet.phone,
                    'address': outlet.address,
                    'state': outlet.state.name
                })
            out['outlets'] = outlets
            return HttpResponse(json.dumps(out))
    return HttpResponseBadRequest("Error in adding device")


def make_token(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=device_id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    pharm = device.pharmacy
    token = randrange(100000, 999999)
    drug_models.Token.objects.create(pharmacy=pharm, code=token)
    return HttpResponse('{}'.format(token))


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


def update_pharm(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    pharmacy = device.pharmacy
    #pharmacy = get_object_or_404(drug_models.Pharmacy, id=id)
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


def add_outlet(request, device_id):
    device = get_object_or_404(drug_models.Device, id=device_id)
    #import pdb;pdb.set_trace()
    form = drug_forms.OutletForm(request.GET)
    if form.is_valid():
        _state = request.GET.get('state')
        state = drug_models.State.objects.get(name__iexact=_state)
        outlet = form.save(commit=False)
        outlet.pharmacy = device.pharmacy
        outlet.state = state
        outlet.active = True
        outlet.save()
        out = {
            'address': outlet.address,
            'state': outlet.state.name,
            'phone': outlet.phone,
            'id': outlet.id
        }
        return HttpResponse(json.dumps(out))
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


def search_drug(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=device_id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    form = drug_forms.SearchForm(request.GET)
    drugs = []
    if form.is_valid():
        item = form.cleaned_data['name'].title()
        drug_models.Search.objects.create(pharmacy=device.pharmacy, name=item)

        for drug in drug_models.Drug.objects.valid_drugs().filter(
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


def stock_drug(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=device_id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    pharmacy = device.pharmacy
    #pharmacy = get_object_or_404(drug_models.Pharmacy, pk=id)
    drugs = []
    for drug in drug_models.Drug.objects.valid_drugs().filter(
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


def wishlist_drug(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=device_id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    pharmacy = device.pharmacy
    #pharmacy = get_object_or_404(drug_models.Pharmacy, pk=pharm_id)
    print "pharmacy %s" % pharmacy
    today = date.today()
    drugs = []
    for item in drug_models.DrugRequest.objects.filter(
            outlet__pharmacy=pharmacy,
            drug__expiry_date__gt=today).filter(
            Q(status=drug_models.DrugRequest.PENDING)
            | Q(status=drug_models.DrugRequest.ACCEPTED)):
        if item.status == drug_models.DrugRequest.PENDING:
            status = "Pending"
        else:
            status = "Accepted"
        drugs.append({
            'id': item.id,
            'name': item.drug.name,
            'brand': item.drug.brand_name,
            'outlet': item.outlet.address,
            'quantity': item.quantity,
            'cost': "{}".format(item.drug.cost),
            'packsize': item.drug.pack_size,
            'expiry': item.drug.expiry_date.strftime('%Y-%m-%d'),
            'status': status,
            'total_cost': "{}".format(item.total_cost)
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


def pending_requests(request, device_id):
    device = get_object_or_404(drug_models.Device, pk=device_id)
    if not device.active:
        return HttpResponseBadRequest('Inactive device')
    pharmacy = device.pharmacy
    print "pharmacy %s" % pharmacy
    today = date.today()
    output = []
    for item in drug_models.DrugRequest.objects.filter(
            drug__outlet__pharmacy=pharmacy,
            drug__expiry_date__gt=today,
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


def feedback(request, id):
    drug_request = get_object_or_404(drug_models.DrugRequest, pk=id)
    form = drug_forms.FeedbackForm(request.GET)
    if form.is_valid():
        drug_models.RequestFeedback.objects.create(
            request=drug_request,
            request_status=drug_request.status,
            message=form.cleaned_data['message'])
        return HttpResponse("Feedback added successfully")
    return HttpResponseBadRequest('Error adding feedback')
