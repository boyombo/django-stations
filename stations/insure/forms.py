from django import forms

from insure.models import Entry, Device


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['id', 'uploaded_on']

    def clean_device(self):
        if 'device' in self.cleaned_data:
            device, _ = Device.objects.get_or_create(
                uuid=self.cleaned_data['device'])
        return device
