from __future__ import unicode_literals
from datetime import datetime, date

from django.contrib.auth.models import User
from django.db import models


class Booking(models.Model):
    resident = models.ForeignKey('Resident', null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    visitors = models.PositiveIntegerField(default=0)
    mode = models.CharField(max_length=50)
    booked_on = models.DateTimeField(default=datetime.now)
    code = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.name


class Estate(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    balance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    @property
    def num_residents(self):
        return self.estate_residents.count()


class Resident(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    #address = models.TextField(blank=True)
    estate = models.ForeignKey(Estate, related_name='estate_residents')
    active = models.BooleanField(default=False)
    registration_date = models.DateField(default=date.today)

    def __unicode__(self):
        return self.name


class Device(models.Model):
    uuid = models.CharField(max_length=200)
    resident = models.ForeignKey(Resident, null=True)
    #code = models.CharField(max_length=10)

    def __unicode__(self):
        return unicode(self.resident)


class Token(models.Model):
    code = models.CharField(max_length=10)
    msisdn = models.CharField(max_length=20)
    uuid = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.msisdn


class MessageTopup(models.Model):
    estate = models.ForeignKey(Estate)
    units = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    when = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return unicode(self.estate)

    def save(self, *args, **kwargs):
        super(MessageTopup, self).save(*args, **kwargs)
        self.estate.balance += self.units
        self.estate.save()


class SentMessage(models.Model):
    resident = models.ForeignKey(Resident)
    when = models.DateField(default=date.today)

    def __unicode__(self):
        return unicode(self.resident)
