from django import forms

from drugshare.models import Pharmacy, Drug, Outlet, Device


class RegisterForm(forms.Form):
    pharmacy = forms.CharField(max_length=200)
    pharmacist = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20)
    email = forms.CharField(max_length=100)
    uuid = forms.CharField(max_length=100)


class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Pharmacy
        exclude = ['registration_date']


class OutletForm(forms.ModelForm):

    class Meta:
        model = Outlet
        exclude = ['pharmacy', 'state']


class DrugForm(forms.ModelForm):

    class Meta:
        model = Drug
        exclude = ['posted_on']


class QtyForm(forms.Form):
    quantity = forms.IntegerField()


class DrugRequestForm(forms.Form):
    quantity = forms.IntegerField()
    outlet = forms.IntegerField()

    def clean_outlet(self):
        if 'outlet' in self.cleaned_data:
            try:
                outlet = Outlet.objects.get(pk=self.cleaned_data['outlet'])
            except Outlet.DoesNotExist:
                raise forms.ValidationError("Outlet does not exist")
            else:
                return outlet


class SearchForm(forms.Form):
    name = forms.CharField(max_length=200)


class UUIDForm(forms.Form):
    uuid = forms.CharField(max_length=200)
    quantity = forms.IntegerField()

    def clean_uuid(self):
        if 'uuid' in self.cleaned_data:
            uuid = self.cleaned_data['uuid']
            try:
                pharmacy = Pharmacy.objects.get(uuid=uuid)
            except Pharmacy.DoesNotExist:
                raise forms.ValidationError("pharmacy does not exist")
            return pharmacy


class StockForm(forms.Form):
    uuid = forms.CharField(max_length=200)


class DeviceForm(forms.Form):
    uuid = forms.CharField(max_length=250)

    def clean_uuid(self):
        if 'uuid' in self.cleaned_data:
            uuid = self.cleaned_data['uuid']
            try:
                device = Device.objects.get(uuid=uuid)
            except Device.DoesNotExist:
                raise forms.ValidationError("device does not exist")
            return device
