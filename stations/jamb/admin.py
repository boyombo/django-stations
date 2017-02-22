from django.contrib import admin

from jamb.models import Exam, Subject, Question


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']


#class AnswerInline(admin.TabularInline):
#    model = Answer


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 50


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['subject', 'year']
    inlines = [QuestionInline]
