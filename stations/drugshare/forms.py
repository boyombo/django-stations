from django import forms

from drugshare.models import Pharmacy, Drug


class PharmacyForm(forms.ModelForm):

    class Meta:
        model = Pharmacy
        exclude = ['registration_date', 'state']


class DrugForm(forms.ModelForm):

    class Meta:
        model = Drug
        exclude = ['pharmacy']
