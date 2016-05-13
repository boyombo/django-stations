from django import forms
from depot.models import Entry, State


def get_states():
    return State.objects.all()


class StationForm(forms.Form):
    brand = forms.CharField(max_length=200)
    address = forms.CharField(max_length=250)
    state = forms.ModelChoiceField(queryset=get_states())
    area = forms.CharField(max_length=250, required=False)

    def clean_area(self):
        if 'area' in self.cleaned_data:
            return [a.strip() for a in self.cleaned_data['area'].split(',')]


class SearchForm(forms.Form):
    name = forms.CharField(max_length=200)


class APISearchForm(forms.Form):
    name = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['station', 'current_time']
