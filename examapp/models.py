#encoding=utf8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Manual(models.Model):
    
    manual = models.CharField(max_length=256, verbose_name=_(u'Manual'))

    class Meta:
        verbose_name = _(u"Manual")
        verbose_name_plural = _(u"Manual")
        app_label = 'examapp'

    def __unicode__(self):
        return u'[%s] %s' % (self.manual, self.subject)


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
    page = models.PositiveSmallIntegerField(verbose_name=_(u'Page'))
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
        verbose_name = _(u"Test Model Subject")
        verbose_name_plural = _(u"Test Model Subjects")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s [%s]' % (self.subject, self.weight)


class TestModelSubject(models.Model):

    test_model = models.ForeignKey(TestModel, verbose_name=_(u'Test Model'))
    subject = models.ForeignKey(Subject, verbose_name=_(u'Subject'))
    weight = models.PositiveSmallIntegerField(verbose_name=_(u'Weight'))

    class Meta:
        verbose_name = _(u"Test Model Subject")
        verbose_name_plural = _(u"Test Model Subjects")
        app_label = 'examapp'

    def __unicode__(self):
        return u'%s [%s]' % (self.subject, self.weight)


