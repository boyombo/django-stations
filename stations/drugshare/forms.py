from django import forms

from drugshare.models import Pharmacy, Drug


class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Pharmacy
        exclude = ['registration_date', 'state']


class DrugForm(forms.ModelForm):

    class Meta:
        model = Drug
        exclude = ['pharmacy', 'posted_on']


class SearchForm(forms.Form):
    name = forms.CharField(max_length=200)
    uuid = forms.CharField(max_length=250)


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


class WishlistForm(forms.Form):
    uuid = forms.CharField(max_length=250)

    def clean_uuid(self):
        if 'uuid' in self.cleaned_data:
            uuid = self.cleaned_data['uuid']
            try:
                pharmacy = Pharmacy.objects.get(uuid=uuid)
            except Pharmacy.DoesNotExist:
                raise forms.ValidationError("pharmacy does not exist")
            return pharmacy
