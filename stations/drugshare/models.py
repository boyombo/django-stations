from __future__ import unicode_literals
from datetime import datetime, date

from django.db import models


class State(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(max_length=200)
    #uuid = models.CharField(max_length=200)
    pharmacist = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    #address = models.CharField(max_length=200, blank=True)
    #area = models.CharField(max_length=200, blank=True)
    #state = models.ForeignKey(State, blank=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    registration_date = models.DateField(default=date.today)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Pharmacies'

    def __unicode__(self):
        return self.name


class Device(models.Model):
    uuid = models.CharField(max_length=200, unique=True)
    pharmacy = models.ForeignKey(Pharmacy)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.uuid


class Outlet(models.Model):
    pharmacy = models.ForeignKey(Pharmacy)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    state = models.ForeignKey(State, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.address


class Drug(models.Model):
    #pharmacy = models.ForeignKey(Pharmacy)
    outlet = models.ForeignKey(Outlet, null=True)
    name = models.CharField('Generic Name', max_length=200)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    pack_size = models.IntegerField(default=1)
    expiry_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    posted_on = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name


class Search(models.Model):
    pharmacy = models.ForeignKey(Pharmacy)
    name = models.CharField(max_length=200)
    when = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Searches'

    def __unicode__(self):
        return self.name


class DrugRequest(models.Model):
    PENDING = 0
    CANCELLED = 1
    ACCEPTED = 2
    DONE = 3
    REQUEST_STATUSES = enumerate(('Pending', 'Cancelled', 'Accepted', 'Done'))

    drug = models.ForeignKey(Drug)
    #pharmacy = models.ForeignKey(Pharmacy)
    outlet = models.ForeignKey(Outlet, null=True)
    quantity = models.IntegerField()
    posted_on = models.DateTimeField(default=datetime.now)
    status = models.PositiveIntegerField(
        choices=REQUEST_STATUSES, default=PENDING)

    def __unicode__(self):
        return unicode(self.drug)

    @property
    def total_cost(self):
        return self.quantity * self.drug.cost

    @property
    def unit_cost(self):
        return self.drug.cost

    @property
    def seller(self):
        return self.drug.outlet.pharmacy

    @property
    def buyer(self):
        return self.outlet.pharmacy

    def save(self, *args, **kwargs):
        super(DrugRequest, self).save_base(*args, **kwargs)
        RequestLog.objects.create(request=self, new_status=self.status)


class RequestLog(models.Model):
    REQUEST_STATUSES = enumerate(('Pending', 'Cancelled', 'Accepted', 'Done'))
    request = models.ForeignKey(DrugRequest)
    when = models.DateTimeField(default=datetime.now)
    new_status = models.PositiveIntegerField(
        choices=REQUEST_STATUSES)

    def __unicode__(self):
        return unicode(self.request)

    @property
    def owner(self):
        return self.request.drug.pharmacy

    @property
    def requesting(self):
        return self.request.pharmacy

    @property
    def drug(self):
        return self.request.drug

    @property
    def status(self):
        return self.get_new_status_display()


class Token(models.Model):
    code = models.CharField(max_length=20)
    pharmacy = models.ForeignKey(Pharmacy)
    when = models.DateField(default=date.today)

    class Meta:
        unique_together = ('code', 'when')

    def __unicode__(self):
        return unicode(self.pharmacy)

    def valid(self):
        return date.today() == self.when
