from django import forms
from depot.models import Entry


class StationForm(forms.Form):
    brand = forms.CharField(max_length=200)
    address = forms.CharField(max_length=250)
    area = forms.CharField(max_length=250, required=False)

    def clean_area(self):
        if 'area' in self.cleaned_data:
            return [a.strip() for a in self.cleaned_data['area'].split(',')]


class SearchForm(forms.Form):
    name = forms.CharField(max_length=200)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['station', 'current_time']
