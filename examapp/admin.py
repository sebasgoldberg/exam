from django.contrib import admin
from examapp.models import *

class AnswerInline(admin.TabularInline):
  model=Answer
  extra=1


class QuestionAdmin(admin.ModelAdmin):
  inlines=[AnswerInline, ]
  list_filter=['subject']
  search_fields=['question', 'answer__answer']
  list_per_page = 40


class TestModelSubjectInline(admin.TabularInline):
  model=TestModelSubject
  extra=1


class TestModelAdmin(admin.ModelAdmin):
  inlines=[TestModelSubjectInline, ]
  search_fields=['test_model']
  list_per_page = 40


admin.site.register(Manual)
admin.site.register(Subject)
admin.site.register(Question,QuestionAdmin)
admin.site.register(TestModel,TestModelAdmin)
admin.site.register(Test)
