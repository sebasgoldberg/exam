#encoding=utf8
from __future__ import print_function
import sys
from django.core.management.base import BaseCommand, CommandError
from examapp.models import *
from django.db.utils import IntegrityError

MANUAL = 0
PAGE = 1
SUBJECT = 2
QUESTION = 3
FIRST_RESPONSE = 4

            
class Command(BaseCommand):
    help = u'Load questions and answers.'

    def add_arguments(self, parser):
        parser.add_argument('ultima', type=int)

    def update_seba(self, *args, **options):
        ultima = options['ultima']

        subject=Subject.objects.filter(subject='Estudadas Seba')[0]
        ultimo=Subject.objects.filter(subject=u'Estudadas Seba Últimas 40')[0]

        t=Test.objects.get(id=170)

        testquestions=t.testquestion_set.all()[0:ultima]

        for tq in testquestions:
            tq.ref_question.other_subjects.add(subject)
            tq.ref_question.other_subjects.remove(ultimo)

        testquestions=t.testquestion_set.all()[ultima-40:ultima]

        for tq in testquestions:
            tq.ref_question.other_subjects.add(ultimo)

        tm=TestModel.objects.get(test_model=u'Estudadas Seba')
        tm.questions = ultima
        tm.save()

    def handle(self, *args, **options):
        self.update_seba(*args,**options)
