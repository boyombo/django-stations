from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from medic.models import Location, BloodType, Subscriber


class AuthForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'Enter your username'
        }
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'Enter your password'
        }
    )

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            #import pdb;pdb.set_trace()
            username = self.cleaned_data['username']
            if username.startswith('+'):
                username = username[1:]
            password = self.cleaned_data['password']
            usr = authenticate(username=username, password=password)
            if not usr:
                raise forms.ValidationError('Wrong credentials')
            return self.cleaned_data


class RegistrationForm(forms.Form):
    mobile = forms.CharField(max_length=20)
    name = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, required=True)
    location = forms.CharField(max_length=100)
    blood_type = forms.CharField(max_length=10)

    def clean_mobile(self):
        if 'mobile' in self.cleaned_data:
            mobile = self.cleaned_data['mobile']
            if mobile.startswith('+'):
                mobile = mobile[1:]
            try:
                User.objects.get(username=mobile)
            except User.DoesNotExist:
                return mobile
            else:
                raise forms.ValidationError('The mobile is already registered')

    def clean_location(self):
        if 'location' in self.cleaned_data:
            try:
                loc = Location.objects.get(pk=self.cleaned_data['location'])
            except Location.DoesNotExist:
                raise forms.ValidationError('The location is invalid')
            else:
                return loc

    def clean_blood_type(self):
        if 'blood_type' in self.cleaned_data:
            try:
                bt = BloodType.objects.get(pk=self.cleaned_data['blood_type'])
            except BloodType.DoesNotExist:
                raise forms.ValidationError('The blood type is invalid')
            else:
                return bt


class RequestForm(forms.Form):
    mobile = forms.CharField(max_length=20)
    comment = forms.CharField(max_length=250)
    location = forms.CharField(max_length=100)
    blood_type = forms.CharField(max_length=10)

    def clean_location(self):
        if 'location' in self.cleaned_data:
            try:
                loc = Location.objects.get(pk=self.cleaned_data['location'])
            except Location.DoesNotExist:
                raise forms.ValidationError('The location is invalid')
            else:
                return loc

    def clean_blood_type(self):
        if 'blood_type' in self.cleaned_data:
            try:
                bt = BloodType.objects.get(pk=self.cleaned_data['blood_type'])
            except BloodType.DoesNotExist:
                raise forms.ValidationError('The blood type is invalid')
            else:
                return bt

    def clean_mobile(self):
        if 'mobile' in self.cleaned_data:
            try:
                sub = Subscriber.objects.get(phone=self.cleaned_data['mobile'])
            except Subscriber.DoesNotExist:
                raise forms.ValidationError('The mobile number is invalid')
            else:
                return sub


class MessageForm(forms.Form):
    mobile = forms.CharField(max_length=20)
    text = forms.CharField(max_length=250)

    def clean_mobile(self):
        if 'mobile' in self.cleaned_data:
            try:
                sub = Subscriber.objects.get(phone=self.cleaned_data['mobile'])
            except Subscriber.DoesNotExist:
                raise forms.ValidationError('The mobile number is invalid')
            else:
                return sub
