from django import forms

from heathen.models import Member


class HeathenForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['location']
