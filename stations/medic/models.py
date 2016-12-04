from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


BLOOD_MAP = {
    'O-': ['O-'],
    'O+': ['O-', 'O+'],
    'A-': ['O-', 'A-'],
    'A+': ['O-', 'O+', 'A-', 'A+'],
    'B-': ['O-', 'B-'],
    'B+': ['O-', 'O+', 'B-', 'B+'],
    'AB-': ['O-', 'A-', 'B-', 'AB-'],
    'AB+': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
}


def is_compatible(donor, recipient):
    if recipient in BLOOD_MAP[donor]:
        return True
    return False


class BloodType(models.Model):
    name = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @property
    def subscriber_count(self):
        return self.subscriber_set.count()

    class Meta:
        ordering = ['name']


class Subscriber(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    blood_type = models.ForeignKey(BloodType)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4)

    def __unicode__(self):
        return self.phone


class BloodRequest(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    blood_type = models.ForeignKey(BloodType)
    location = models.ForeignKey(Location)
    comment = models.TextField()
    when = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.subscriber)


class Message(models.Model):
    text = models.TextField()
    request = models.ForeignKey(BloodRequest)
    subscriber = models.ForeignKey(Subscriber)
    when = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.text


class Candidate(models.Model):
    blood_request = models.ForeignKey(BloodRequest)
    subscriber = models.ForeignKey(Subscriber)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.subscriber)

    @property
    def owner(self):
        return self.subscriber == self.blood_request.subscriber
