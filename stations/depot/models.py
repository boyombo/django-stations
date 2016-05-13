from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Station(models.Model):
    brand = models.ForeignKey(Brand)
    address = models.CharField(max_length=250)
    area = models.ManyToManyField(Area, related_name='station_areas')
    state = models.ForeignKey(State, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.brand)

    @property
    def recent(self):
        entries = self.station_entries.order_by('-current_time')
        if entries:
            return entries[0]


class Entry(models.Model):
    FEW = 0
    AVERAGE = 1
    MANY = 2
    NUM_CARS = ((FEW, '1 - 10'), (AVERAGE, '11 - 20'), (MANY, '> 20'))
    station = models.ForeignKey(Station, related_name='station_entries')
    num_cars = models.PositiveIntegerField(
        choices=NUM_CARS, null=True, blank=True)
    fuel_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    kegs = models.BooleanField(default=False)
    current_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return unicode(self.station)
