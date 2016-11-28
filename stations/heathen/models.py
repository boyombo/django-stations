from __future__ import unicode_literals

from django.db import models


class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'
        ordering = ['name']


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @property
    def member_count(self):
        return self.member_set.count()

    class Meta:
        ordering = ['name']


class Member(models.Model):
    UNAVAILABLE = 0
    AVAILABLE = 1
    STATUS = ((0, 'Unavailable'), (1, 'Available'))
    MALE = 0
    FEMALE = 1
    GENDERS = ((0, 'Female'), (1, 'Male'))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.ForeignKey(Location)
    birthday = models.DateField()
    availability = models.PositiveIntegerField(choices=STATUS)
    gender = models.PositiveIntegerField(choices=GENDERS, null=True)
    industry = models.ForeignKey(Industry, null=True)
    nok_name = models.CharField(max_length=50, blank=True)
    nok_phone = models.CharField(max_length=20, blank=True)
    nok_email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.email
