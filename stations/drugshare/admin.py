from django.contrib import admin

from drugshare.models import State, Pharmacy, Drug


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid', 'phone', 'area', 'state']


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['pharmacy', 'name', 'expiry_date', 'cost', 'quantity']
    list_filter = ['pharmacy']
    search_fields = ['name']
    date_heirarchy = 'expiry_date'
