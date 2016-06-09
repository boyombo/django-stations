from django.contrib import admin

from drugshare.models import State, Pharmacy, Drug,\
    Search, DrugRequest, RequestLog, Outlet, Device


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['name', 'when', 'pharmacy']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'pharmacy', 'active']


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'registration_date']


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'brand_name', 'name',
                    'expiry_date', 'cost', 'quantity']
    list_filter = ['outlet__pharmacy']
    search_fields = ['name']
    date_hierarchy = 'expiry_date'


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'requesting', 'drug', 'when', 'status']
    search_fields = ['request__drug__pharmacy__name',
                     'request__pharmacy__name']
    date_hierarchy = 'when'
    list_filter = ['new_status']


@admin.register(DrugRequest)
class DrugRequestAdmin(admin.ModelAdmin):
    list_display = ['drug', 'seller', 'buyer', 'outlet', 'quantity',
                    'posted_on', 'status', 'unit_cost', 'total_cost']
    date_hierarchy = 'posted_on'


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ['pharmacy', 'phone', 'address', 'state', 'active']
