from django.contrib import admin

from parcel.models import State, Location, Vehicle, Parcel, Client


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'address']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address', 'state']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['licence_plate', 'location', 'in_transit']


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ['description', 'waybill', 'sender', 'recipient_phone',
                    'loaded_from', 'destination', 'status', 'current_location']
