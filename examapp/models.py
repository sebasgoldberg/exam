#encoding=utf8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from random import randint


class ExamException(Exception):
    pass


class QuestionsQuantityError(ExamException):
    pass


class Manual(models.Model):
    
    manual = models.CharField(max_length=256, verbose_name=_(u'Manual'))

    class Meta:
        verbose_name = _(u"Manual")
        verbose_name_plural = _(u"Manual")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s' % self.manual


class Subject(models.Model):
    
    manual = models.ForeignKey(Manual, verbose_name=_(u'Manual'))
    subject = models.CharField(max_length=256, verbose_name=_(u'Subject'))

    class Meta:
        verbose_name = _(u"Subject")
        verbose_name_plural = _(u"Subjects")
        app_label = 'examapp'

    def __unicode__(self):
        return u'[%s] %s' % (self.manual, self.subject)


class Question(models.Model):
    
    subject = models.ForeignKey(Subject, verbose_name=_(u'Subject'))
    page = models.PositiveSmallIntegerField(verbose_name=_(u'Page'), blank=True, null=True)
    question = models.TextField(verbose_name=_(u'Question'))

    class Meta:
        verbose_name = _(u"Question")
        verbose_name_plural = _(u"Questions")
        app_label = 'examapp'

    def __unicode__(self):
        return u'[%s] [%s] %s' % (self.subject, self.page, self.question)

    def acoes(self):
        return u"<a href='/default/dashboard_secao?cod_secao=%s' target='_blank'>%s</a>" % (
            self.cod_secao,_(u'Dashboard'))
    acoes.allow_tags = True
    acoes.short_description = _(u'Ações')


class Answer(models.Model):
    
    question = models.ForeignKey(Question, verbose_name=_(u'Question'))
    answer = models.TextField(verbose_name=_(u'Answer'))
    is_correct = models.BooleanField(verbose_name=_(u'Is Correct?'), default=False)

    class Meta:
        verbose_name = _(u"Answer")
        verbose_name_plural = _(u"Answers")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s' % (self.answer)


class TestModel(models.Model):

    test_model = models.CharField(max_length=256, verbose_name=_(u'Test Model'))
    questions = models.PositiveSmallIntegerField(verbose_name=_(u'Number of questions'))

    class Meta:
        verbose_name = _(u"Test Model")
        verbose_name_plural = _(u"Test Models")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s' % self.test_model

    def random_weights(self):
        total_weight = 0
        tms_weights = []
        for tms in self.testmodelsubject_set.all():
            weight = float(tms.random_weight())
            tms_weights.append((tms, weight,))
            total_weight = total_weight + tms.random_weight() 
        return (tms_weights, total_weight)

    def create_test(self):
        t=Test.objects.create(test_model=self)

        tms_weights, total_weight = self.random_weights()

        total_questions = 0
        for tms, weight in tms_weights[:-1]:
            questions = self.questions * (
                weight / total_weight )
            total_questions = total_questions + len(create_random_test_questions(tms, questions))
        
        tms, weight = tms_weights[-1]
        total_questions = total_questions + len(t.create_random_test_questions(tms, self.questions - total_questions))

        if total_questions <> self.questions:
            raise QuestionsQuantityError()

        return t

class TestModelSubject(models.Model):

    test_model = models.ForeignKey(TestModel, verbose_name=_(u'Test Model'))
    subject = models.ForeignKey(Subject, verbose_name=_(u'Subject'))
    weight_from = models.PositiveSmallIntegerField(verbose_name=_(u'Weight from'))
    weight_to = models.PositiveSmallIntegerField(verbose_name=_(u'Weight to'))

    class Meta:
        verbose_name = _(u"Test Model Subject")
        verbose_name_plural = _(u"Test Model Subjects")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s [%s-%s]' % (self.subject, self.weight_from, self.weight_to)

    def random_weight(self):
       return randint(self.weight_from, self.weight_to) 

    def random_questions(self, n):
        for q in self.subject.question_set.order_by('?')[:n]:
            yield q

class Test(models.Model):
    test_model = models.ForeignKey(TestModel, verbose_name=_(u'Test Model'))

    def create_random_test_questions(self, tms, n):
        result = []
        for q in tms.random_questions(n):
            tq = self.testquestion_set.create(
                ref_question=q,
                test=self)

            tq.create_test_answers()

            result.append(tq)

        return result

    def get_test_note(self):
        self.testquestions
        for tq in self.test

class TestQuestion(models.Model):
    ref_question = models.ForeignKey(Question, verbose_name=_(u'Question'))
    test = models.ForeignKey(Test, verbose_name=_(u'Test'))

    def create_test_answers(self):
        for a in self.ref_question.answer_set.all():
            self.testanswer_set.create(
                ref_answer = a,
                test_question = self
            )

class TestAnswer(models.Model):
    ref_answer = models.ForeignKey(Answer, verbose_name=_(u'Answer'))
    test_question = models.ForeignKey(TestQuestion, verbose_name=_(u'Test Question'))
    is_correct = models.BooleanField(verbose_name=_(u'Is Correct?'), default=False)
