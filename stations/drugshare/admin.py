from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from drugshare.models import State, Pharmacy, Drug,\
    Search, DrugRequest, RequestLog, Outlet, Device, Token


class ExpiredListFilter(admin.SimpleListFilter):
    title = _('expired')
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('expired')),
            ('no', _('not expired'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(expiry_date__lte=date.today())
        else:
            return queryset.filter(expiry_date__gt=date.today())


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
    list_display = ['name', 'phone', 'email', 'verified', 'registration_date']
    actions = ['mark_verified']

    def mark_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_verified.short_description = 'Verify the selected pharmacies'


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['outlet', 'pharmacy', 'brand_name', 'name',
                    'expiry_date', 'email', 'phone', 'cost', 'quantity']
    list_filter = [ExpiredListFilter, 'outlet__pharmacy']
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


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['code', 'pharmacy', 'when', 'valid']


admin.site.disable_action('delete_selected')
