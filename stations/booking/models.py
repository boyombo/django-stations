from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class Booking(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    visitors = models.PositiveIntegerField(default=0)
    mode = models.CharField(max_length=50)
    booked_on = models.DateTimeField(default=datetime.now)
    code = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.name
