from __future__ import unicode_literals

from django.db import models


class BusinessType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=20, blank=True)
    business_kind = models.ForeignKey(BusinessType)
    location = models.TextField(blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    licence_no = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def __unicode__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.CharField('Serial', max_length=20, blank=True)
    business = models.ForeignKey(Business)
    amount = models.PositiveIntegerField()
    date_of_payment = models.DateField()
    expiration_date = models.DateField()

    def __unicode__(self):
        return unicode(self.business)
