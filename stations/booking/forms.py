from django import forms

from booking.models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'visitors', 'mode']
