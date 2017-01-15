from django import forms

from parcel.models import Client, Parcel, Location, Vehicle


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = []


class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        exclude = ['status', 'sender', 'current_location',
                   'loaded_on', 'delivered_on', 'collected_on']


class LoadForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    parcels = forms.ModelMultipleChoiceField(
        queryset=Parcel.objects.all(),
        widget=forms.CheckboxSelectMultiple())


class ArrivalForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    parcels = forms.ModelMultipleChoiceField(
        queryset=Parcel.objects.all(),
        widget=forms.CheckboxSelectMultiple())


class SearchForm(forms.Form):
    term = forms.CharField(max_length=50)


class StatusForm(forms.Form):
    waybill = forms.CharField(max_length=50)

    def clean_waybill(self):
        if 'waybill' in self.cleaned_data:
            try:
                parcel = Parcel.objects.get(
                    waybill__iexact=self.cleaned_data['waybill'])
            except Parcel.DoesNotExist:
                raise forms.ValidationError(
                    'The waybill number you entered is invalid')
            else:
                return parcel
