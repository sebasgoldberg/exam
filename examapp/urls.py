from django.conf.urls import url

from examapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<test_model_id>[0-9]+)/new/$', views.new, name='new'),
    url(r'^(?P<test_id>[0-9]+)/test/$', views.test, name='test'),
    url(r'^(?P<test_id>[0-9]+)/result/$', views.result, name='result'),
    url(r'^(?P<test_question_id>[0-9]+)/question/$', views.question, name='question'),
    ]
