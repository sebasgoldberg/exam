from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from examapp.models import *
from examapp.forms import *

def index(request):
    template = loader.get_template('examapp/index.html')
    context = {
        'test_models': TestModel.objects.all(),
        }
    return HttpResponse(template.render(context, request))

def new(request, test_model_id):
    tm = TestModel.objects.get(id=test_model_id)
    return redirect('test', test_id=tm.create_test().id)

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
