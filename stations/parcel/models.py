from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class State(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Client(models.Model):
    MALE = 0
    FEMALE = 1
    GENDERS = ((0, 'Male'), (1, 'Female'))

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    address = models.CharField(max_length=100)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.address


class Vehicle(models.Model):
    licence_plate = models.CharField(max_length=10)
    location = models.ForeignKey(Location, null=True, blank=True)
    in_transit = models.BooleanField(default=False)

    def __unicode__(self):
        return self.licence_plate


class Parcel(models.Model):
    LOADING = 0
    TRANSIT = 1
    ARRIVED = 2
    COLLECTED = 3
    STATUS = enumerate(('Loading', 'Transit', 'Arrived', 'Collected'))

    description = models.TextField()
    waybill = models.CharField(max_length=50, unique=True)
    sender = models.ForeignKey(Client)
    recipient_name = models.CharField(max_length=50)
    recipient_phone = models.CharField(max_length=20)
    loaded_from = models.ForeignKey(Location, related_name='origin')
    destination = models.ForeignKey(Location, related_name='destination')
    status = models.PositiveIntegerField(choices=STATUS)
    current_location = models.ForeignKey(
        Location, related_name='parcel_location')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.ForeignKey(Vehicle, null=True)
    batch_number = models.CharField(max_length=20, blank=True)
    loaded_on = models.DateTimeField(default=timezone.now)
    delivered_on = models.DateTimeField(null=True, blank=True)
    collected_on = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.waybill
