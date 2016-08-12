from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from examapp.models import *
from examapp.forms import *

def add_test_to_last_tests(request, test_id):
    last_tests = request.session.get('last_tests', [])
    if test_id in last_tests:
        return
    last_tests.insert(0,test_id)
    request.session['last_tests'] = last_tests

def index(request):
    template = loader.get_template('examapp/index.html')
    context = {
        'test_models': TestModel.objects.all(),
        'last_tests': [ Test.objects.get(id=x) for x in request.session.get('last_tests', []) ]
        }
    return HttpResponse(template.render(context, request))

def new(request, test_model_id):
    tm = TestModel.objects.get(id=test_model_id)
    t = tm.create_test()
    add_test_to_last_tests(request, t.id)
    return redirect('question', test_question_id=t.testquestion_set.get(question_number=1).id)

def test(request, test_id):
    return redirect('result', test_id=test_id)
    template = loader.get_template('examapp/test.html')
    context = {
        'test': Test.objects.get(id=test_id),
        }
    return HttpResponse(template.render(context, request))

from django.db import transaction

@transaction.atomic
def result(request, test_id):

    t = Test.objects.get(id=test_id)
    if request.method == 'POST':
        f = TestForm(t, request.POST)
        if f.is_valid():
            for a in t.iter_test_answers():
                a.is_correct = f.cleaned_data['A%s'%a.id]
                a.save()
            t.refresh_from_db()

    note = t.get_test_note()
    template = loader.get_template('examapp/test.html')
    context = {
        'note': note * 100,
        'test': t,
        }

    return HttpResponse(template.render(context, request))


def question(request, test_question_id):
    tq = TestQuestion.objects.get(id=test_question_id)
    if request.method == 'POST':
        f = TestForm(tq.test, request.POST)
        if f.is_valid():
            for a in tq.testanswer_set.all():
                a.is_correct = f.cleaned_data['A%s'%a.id]
                a.save()
            tq.refresh_from_db()

    try:
        previous_test_question = tq.get_previous_question_id()
    except TestQuestion.DoesNotExist:
        previous_test_question = 0
    try:
        next_test_question = tq.get_next_question_id()
    except TestQuestion.DoesNotExist:
        next_test_question = 0
    note = tq.test.get_test_note()
    template = loader.get_template('examapp/question.html')
    context = {
        'note': note * 100,
        'tq': tq,
        'previous_test_question': previous_test_question,
        'next_test_question': next_test_question
        }

    return HttpResponse(template.render(context, request))



