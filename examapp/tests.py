from django.test import TestCase
from examapp.models import *

class TestExam(TestCase):

    def setUp(self):

        self.manual = Manual.objects.create()
        self.subject = Subject.objects.create(manual=self.manual)

        self.Q1 = Question.objects.create(
            subject=self.subject,
            question=u'Q1')

        self.Q1A1 = self.Q1.answer_set.create(
            answer=u'A1',
            is_correct=True
            )

        self.Q1A2 = Answer.objects.create(
            question=self.Q1,
            answer=u'A2',
            is_correct=False
            )

        self.TM = TestModel.objects.create(questions=1)

        self.TM.testmodelsubject_set.create(
            subject=self.subject,
            weight_from=1,
            weight_to=1)

    def test_create_random_test_questions(self):

        T = self.TM.create_test()

        questions = T.create_random_test_questions(
            self.subject.testmodelsubject_set.first(),1)

        self.assertEqual(len(questions),1)

    def test_random_weights(self):

        tms_weights, total_weight = self.TM.random_weights()

        self.assertEqual(total_weight,1)
        self.assertEqual(len(tms_weights),1)

    def test_exam_test(self):

        T = self.TM.create_test()

        self.assertEqual(T.testquestion_set.count(), 1)

        TQ1 = T.testquestion_set.all()[0]

        self.assertEqual(TQ1.testanswer_set.count(), 2)

        TQ1A1 = TQ1.testanswer_set.get(ref_answer__answer='A1')
        TQ1A2 = TQ1.testanswer_set.get(ref_answer__answer='A2')

        TQ1A1.is_correct = True
        TQ1A1.save()

        TQ1A2.is_correct = False
        TQ1A2.save()
        
        note = T.get_test_note()

        self.assertEqual(note, 1)
