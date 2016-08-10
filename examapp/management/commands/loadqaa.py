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
        parser.add_argument('filepath', nargs='+')

    def loadqaa_unformated(self, *args, **options):

        subject = Subject.objects.get_or_create(subject='Retail')[0]
        
        with open('loadqaa.err', 'w') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:

                    question_mode = False
                    response_mode = False
                    question_text = u''
                    question = None

                    for line in f:

                        sys.stdout.write(line)

                        if line.strip('\r\n').split() == '':
                            continue

                        if 'Question' in line:
                            question_mode = True
                            response_mode = False
                            question_text = u''
                            question = None
                            continue

                        if 'Response' in line:
                            question = Question.objects.get_or_create(
                                subject=subject,
                                question=question_text
                                )[0]
                            question_mode = False
                            response_mode = True
                            continue

                        if question_mode:
                            question_text = '%s%s' % (question_text, line)

                        if response_mode:
                            try:
                                is_correct, response_text = line.strip('\r\n').split('\t')
                            except ValueError:
                                continue
                            is_correct = ( is_correct == 'X' )

                            question.answer_set.create(
                                answer = response_text,
                                is_correct = is_correct
                            )


    def handle(self, *args, **options):
        
        self.loadqaa_unformated(*args,**options)

        return

        with open('loadqaa.err', 'w') as ferr:

            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:

                        if header:
                            header = False
                            continue

                        register = line.strip('\r\n').split('\t')

                        if len(register) < 6:
                            self.stdout.write(self.style.ERROR(u'ERROR: Quantity of fields %s: %s' % (len(register), register)))
                            print(line,file=ferr)
                            continue

                        for i in range(len(register)):
                            register[i] = register[i].strip()


                        try:

                            try:

                                try:
                                    
                                    manual = None
                                    
                                    if register[MANUAL] != '':

                                        manual = Manual.objects.get(
                                            manual=register[MANUAL]
                                            )

                                except Manual.DoesNotExist:
                                    
                                    manual = Manual.objects.create(
                                        manual=register[MANUAL]
                                        )

                                    manual.refresh_from_db()

                            except IntegrityError:
                                self.stdout.write(self.style.ERROR(u'ERROR: Integrity error when trying to create manual: %s' % register))
                                print(line.strip(),file=ferr)
                                continue


                            try:
                                
                                try:

                                    subject = Subject.objects.get(
                                        subject = register[SUBJECT],
                                        )

                                except Subject.DoesNotExist:

                                    subject = Subject.objects.create(
                                        subject = register[SUBJECT],
                                        )

                                    subject.refresh_from_db()

                            except IntegrityError:
                                self.stdout.write(self.style.ERROR(u'ERROR: Integrity error when trying to create subject: %s' % register))
                                print(line.strip(),file=ferr)
                                continue

                            try:

                                try:

                                    if register[PAGE] == '':
                                        page = 0
                                    else:
                                        page = register[PAGE]


                                    question = Question.objects.get(
                                        subject=subject,
                                        manual=manual,
                                        page=page,
                                        question=register[QUESTION]
                                        )

                                except Question.DoesNotExist:

                                    question = Question.objects.create(
                                        subject=subject,
                                        manual=manual,
                                        page=page,
                                        question=register[QUESTION]
                                        )

                                    question.refresh_from_db()

                                    self.stdout.write(self.style.SUCCESS(u'Question "%s" successfully created.' % question))

                                Answer.objects.filter(question=question).delete()
                                question.refresh_from_db()

                                for i in range(FIRST_RESPONSE,len(register),2):
                                    if register[i] == '':
                                        continue
                                    is_correct = ( register[i+1] != '' )

                                    question.answer_set.create(
                                        answer = register[i],
                                        is_correct = is_correct
                                    )

                            except IntegrityError:
                                self.stdout.write(self.style.ERROR(u'ERROR: Integrity error when trying to create question or answer: %s' % register))
                                print(line.strip(),file=ferr)
                                continue

                        except UnicodeDecodeError:
                            self.stdout.write(self.style.ERROR(u'ERRO: Erro unicode no registro: %s' % register ))
                            print(line.strip(),file=ferr)
                            

