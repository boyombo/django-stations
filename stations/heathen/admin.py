from django.contrib import admin

from heathen.models import Location, Member, Industry


@admin.register(Location, Industry)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'location']
    list_filter = ['location']
