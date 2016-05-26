from django import forms

from insure.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['id']
