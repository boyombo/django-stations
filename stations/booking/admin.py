from django.contrib import admin

from booking.models import Booking, Estate, Resident, Token, Device,\
    MessageTopup, SentMessage


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['resident', 'name', 'phone',
                    'visitors', 'mode', 'booked_on', 'code']


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone', 'balance',
                    'address', 'num_residents']


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'estate', 'active', 'registration_date']


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['code', 'msisdn']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'resident']


@admin.register(MessageTopup)
class MessageTopupAdmin(admin.ModelAdmin):
    list_display = ['estate', 'units', 'amount', 'when']
    search_fields = ['estate__name']


@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
    list_display = ['resident', 'when']
    search_fields = ['resident__phone', 'resident__name',
                     'resident__estate__name']
