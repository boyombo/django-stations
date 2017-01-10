#from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
#from django.contrib.auth.models import User
from tax.models import Payment


def json_response(params, success):
    if success:
        params.update({'success': 'true'})
    else:
        params.update({'success': 'false'})
    return HttpResponse(json.dumps(params))


def auth(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    usr = authenticate(username=username, password=password)
    if not usr:
        return json_response({'msg': 'Wrong credentials'}, False)
    else:
        return json_response({}, True)


def search(request):
    term = request.GET.get('serial')
    try:
        payment = Payment.objects.get(payment_id=term)
    except Payment.DoesNotExist:
        return json_response({'msg': 'Invalid Serial'}, False)
    else:
        params = {
            'name': payment.business.name,
            'kind': payment.business.business_kind.name,
            'location': payment.business.location,
            'vehicle_type': payment.business.vehicle_type,
            'licence_no': payment.business.licence_no,
            'amount': payment.amount,
            'payment_date': payment.date_of_payment.strftime('%d %b %Y'),
            'expiry_date': payment.expiration_date.strftime('%d %b %Y'),
            'show_vehicle': payment.business.is_vehicle
        }
        return json_response({'details': params}, True)
