from django import forms

from booking.models import Booking, Resident


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'visitors', 'mode']


class ResidentForm(forms.ModelForm):

    class Meta:
        model = Resident
        exclude = ['estate', 'registration_date']
