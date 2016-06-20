from django import forms
from django.contrib.auth.models import User

from booking.models import Booking, Resident


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'visitors', 'mode']


class ResidentForm(forms.ModelForm):

    class Meta:
        model = Resident
        exclude = ['estate', 'registration_date']


class SearchForm(forms.Form):
    term = forms.CharField(max_length=20)


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea())
    username = forms.CharField(max_length=100)
    pwd1 = forms.CharField(widget=forms.PasswordInput())
    pwd2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            if self.cleaned_data['pwd1'] != self.cleaned_data['pwd2']:
                raise forms.ValidationError('Your passwords dont match')
            return self.cleaned_data

    def clean_username(self):
        if 'username' in self.cleaned_data:
            try:
                User.objects.get(username=self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
            else:
                raise forms.ValidationError('The username is already taken')
