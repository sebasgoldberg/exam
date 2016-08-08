from django import forms

class TestForm(forms.Form):

    def __init__(self, test, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        for q in test.testquestion_set.all():
            for a in q.testanswer_set.all():
                self.fields['A%s' % a.id] = forms.BooleanField(required=False)
