from __future__ import unicode_literals

from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Exam(models.Model):
    subject = models.ForeignKey(Subject)
    year = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.subject)


class Question(models.Model):
    CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'))
    exam = models.ForeignKey(Exam)
    text = models.TextField()
    pic = models.ImageField(upload_to='questions', null=True, blank=True)
    answer_A = models.CharField(max_length=150, blank=True)
    answer_B = models.CharField(max_length=150, blank=True)
    answer_C = models.CharField(max_length=150, blank=True)
    answer_D = models.CharField(max_length=150, blank=True)
    answer_E = models.CharField(max_length=150, blank=True)
    correct = models.CharField(max_length=5, choices=CHOICES, null=True, blank=True)

    def __unicode__(self):
        return self.text


#class Answer(models.Model):
#    CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'))
#    question = models.ForeignKey(Question)
#    label = models.CharField(max_length=5, choices=CHOICES)
#    text = models.CharField(max_length=150)
#    correct = models.BooleanField(default=False)
#
#    def __unicode__(self):
#        return self.text
