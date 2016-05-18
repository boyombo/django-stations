from django.contrib import admin

from depot.models import Brand, Area, Station, Entry, State


@admin.register(Brand, Area, State)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['brand', 'address', 'state', 'longitude', 'latitude']
    filter_horizontal = ('area', )


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['station', 'num_cars', 'fuel_price', 'current_time']
