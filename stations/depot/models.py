from __future__ import unicode_literals
from datetime import datetime

from django.db import models


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
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.brand)


class Entry(models.Model):
    station = models.ForeignKey(Station, related_name='station_entries')
    num_cars = models.PositiveIntegerField()
    fuel_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return unicode(self.station)
