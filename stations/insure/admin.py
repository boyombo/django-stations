from django.contrib import admin

from insure.models import Entry, Device


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['admin_image', 'address', 'developer', 'insurance_type',
                    'position', 'device']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name']
