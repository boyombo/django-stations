from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.safestring import mark_safe


class Device(models.Model):
    uuid = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    address = models.CharField(max_length=200, blank=True)
    developer = models.CharField(max_length=200, blank=True)
    building_type = models.CharField(max_length=200, blank=True)
    consultants = models.CharField(max_length=200, blank=True)
    contractors = models.CharField(max_length=200, blank=True)
    insurance_type = models.CharField(max_length=200, blank=True)
    rep = models.CharField('Representative', max_length=200, blank=True)
    foreman = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=200, blank=True)
    height = models.CharField(max_length=200, blank=True)
    basement = models.CharField(max_length=200, blank=True)
    floors = models.CharField(max_length=200, blank=True)
    building = models.ImageField('Building Image', upload_to='pictures')
    longitude = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    uploaded_on = models.DateTimeField(default=datetime.now, blank=True)
    device = models.ForeignKey(Device, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.address

    def admin_image(self):
        return mark_safe(
            '<img src="%s" height=100 width=100 />' % self.building.url)
    admin_image.allow_tags = True

    def position(self):
        return u'{}, {}'.format(self.latitude[:7], self.longitude[:7])
