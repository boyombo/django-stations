from __future__ import unicode_literals
from datetime import datetime, date

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(max_length=200, unique=True)
    uuid = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=200, blank=True)
    area = models.CharField(max_length=200, blank=True)
    state = models.ForeignKey(State, blank=True)
    registration_date = models.DateField(default=date.today)

    class Meta:
        verbose_name_plural = 'Pharmacies'

    def __unicode__(self):
        return self.name


class Drug(models.Model):
    pharmacy = models.ForeignKey(Pharmacy)
    name = models.CharField(max_length=200)
    expiry_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    posted_on = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name
