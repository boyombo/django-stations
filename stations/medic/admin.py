from django.contrib import admin

from medic.models import BloodType, Location, Subscriber, BloodRequest,\
    Message, Candidate, BloodBank


@admin.register(BloodType, Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'name', 'location', 'blood_type',
        'verified', 'verification_code']


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'blood_type', 'location', 'when', 'comment']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'request', 'when', 'text']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['blood_request', 'subscriber', 'active']


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'location', 'latitude']
