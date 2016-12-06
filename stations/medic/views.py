from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from random import randrange

from medic.forms import AuthForm, RegistrationForm, RequestForm, MessageForm
from medic.models import Location, BloodType, Subscriber, BloodRequest,\
    Message, Candidate
from api.sms import send_message


def get_blood_types():
    return [
        {
            'id': bt.id,
            'name': bt.name
        } for bt in BloodType.objects.all()
    ]


def get_locations():
    return [
        {
            'id': loc.id,
            'name': loc.name
        } for loc in Location.objects.all()
    ]


def initdata(request):
    out = {
        'status': 'Ok',
        'success': 'true',
        'locations': get_locations(),
        'blood_types': get_blood_types()
    }
    print out
    return HttpResponse(json.dumps(out))


def get_stats(sub):
    return {
        'location': sub.location.name,
        'blood_type': sub.blood_type.name,
        'verified': 'true' if sub.verified else 'false',
        'name': sub.name,
        'count': Subscriber.objects.count(),
        'loc_count': Subscriber.objects.filter(location=sub.location).count()
    }


@csrf_exempt
def authenticate(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            #user = User.objects.get(username=form.cleaned_data['username'])
            mobile = form.cleaned_data['username']
            subscriber = Subscriber.objects.get(phone=mobile)
            out = {
                'token': str(form.cleaned_data['username']),
                'status': 'Ok',
                'success': 'true',
            }
            out.update(get_stats(subscriber))
            print out
            return HttpResponse(json.dumps(out))
        else:
            #import pdb;pdb.set_trace()
            errors = {k: v[0] for k, v in form.errors.items()}
    out = json.dumps({'msg': errors, 'success': 'false'})
    print out
    return HttpResponse(out)


@csrf_exempt
def register(request):
    errors = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            # create user
            user = User.objects.create_user(
                username=form.cleaned_data['mobile'],
                password=form.cleaned_data['password'])
            # verification code
            code = '{}'.format(randrange(1234, 9899))
            # subscriber
            subscriber = Subscriber.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['mobile'],
                location=form.cleaned_data['location'],
                blood_type=form.cleaned_data['blood_type'],
                verified=False,
                verification_code=code)
            #user = User.objects.get(username=form.cleaned_data['username'])
            out = {
                'token': form.cleaned_data['mobile'],
                'status': 'Ok',
                'success': 'true',
                'location': form.cleaned_data['location'].name,
                'blood_type': form.cleaned_data['blood_type'].name,
                'name': form.cleaned_data['name']
            }
            out.update(get_stats(subscriber))
            print out
            mobile = form.cleaned_data['mobile']
            msg = 'Verification code for Med-Info is {}'.format(code)
            send_message(mobile, msg)
            return HttpResponse(json.dumps(out))
        else:
            #import pdb;pdb.set_trace()
            errors = {k: v[0] for k, v in form.errors.items()}
    out = json.dumps({'msg': errors, 'success': 'false'})
    print out
    return HttpResponse(out)


def verify(request):
    mobile = request.GET.get('mobile')
    code = request.GET.get('code')
    try:
        sub = Subscriber.objects.get(phone=mobile, verification_code=code)
    except Subscriber.DoesNotExist:
        out = {'msg': 'Wrong number/code', 'success': 'false'}
    else:
        sub.verified = True
        sub.save()
        out = {'status': 'Ok', 'success': 'true'}
    return HttpResponse(json.dumps(out))


@csrf_exempt
def makerequest(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = RequestForm(request.POST)
        if form.is_valid():
            br = BloodRequest.objects.create(
                subscriber=form.cleaned_data['mobile'],
                comment=form.cleaned_data['comment'],
                location=form.cleaned_data['location'],
                blood_type=form.cleaned_data['blood_type'])

            Message.objects.create(
                text=form.cleaned_data['comment'],
                request=br,
                subscriber=form.cleaned_data['mobile'])

            Candidate.objects.create(
                blood_request=br,
                subscriber=form.cleaned_data['mobile'],
                active=True)

            out = {'status': 'Ok', 'success': 'true'}
            return HttpResponse(json.dumps(out))
    return HttpResponse(json.dumps({'success': 'false'}))


def myrequests(request):
    mobile = request.GET.get('mobile')
    sub = Subscriber.objects.get(phone=mobile)
    candidates = [
        {
            'id': cnd.blood_request.id,
            'blood_type': cnd.blood_request.blood_type.name,
            'location': cnd.blood_request.location.name,
            'comment': cnd.blood_request.comment,
            'when': cnd.blood_request.when.strftime('%d %b %y %H:%M %p')
        } for cnd in Candidate.objects.filter(subscriber=sub)
    ]
    #my_requests = [
    #    {
    #        'id': rqst.id,
    #        'blood_type': rqst.blood_type.name,
    #        'location': rqst.location.name,
    #        'comment': rqst.comment,
    #        'when': rqst.when.strftime('%d %b %y %H:%M %p')
    #    } for rqst in BloodRequest.objects.filter(subscriber=sub)
    #]
    out = {
        'status': 'Ok',
        'success': 'true',
        'requests': candidates
    }
    return HttpResponse(json.dumps(out))


def get_request_messages(req, mobile):
    messages = []
    for msg in Message.objects.filter(request=req):
        line = {
            'id': msg.id,
            'from': msg.subscriber.phone,
            'location': msg.subscriber.location.name,
            'when': msg.when.strftime('%d %b %y %H:%M %p'),
            'text': msg.text
        }
        if mobile == msg.subscriber.phone:
            line['from'] = 'Me'
        messages.append(line)
    return messages


def get_messages(request, id):
    rqst = get_object_or_404(BloodRequest, pk=id)
    mobile = request.GET.get('mobile')
    messages = get_request_messages(rqst, mobile)
    #for msg in Message.objects.filter(request=rqst):
    #    line = {
    #        'id': msg.id,
    #        'from': msg.subscriber.phone,
    #        'location': msg.subscriber.location.name,
    #        'when': msg.when.strftime('%d %b %y %H:%M %p'),
    #        'text': msg.text
    #    }
    #    if mobile == msg.subscriber.phone:
    #        line['from'] = 'Me'
    #    messages.append(line)
    out = {
        'status': 'Ok',
        'success': 'true',
        'messages': messages
    }
    print out
    return HttpResponse(json.dumps(out))


@csrf_exempt
def add_message(request, id):
    rqst = get_object_or_404(BloodRequest, pk=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            sub = form.cleaned_data['mobile']
            text = form.cleaned_data['text']
            Message.objects.create(
                text=text,
                request=rqst,
                subscriber=sub)
        messages = get_request_messages(rqst, sub.phone)
        out = {
            'status': 'Ok',
            'success': 'true',
            'messages': messages
        }
        return HttpResponse(json.dumps(out))
