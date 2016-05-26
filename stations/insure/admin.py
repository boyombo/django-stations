from django.contrib import admin

from insure.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['admin_image', 'address', 'developer', 'insurance_type',
                    'longitude', 'latitude']
