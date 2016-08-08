from django.test import TestCase
from examapp.models import *

class TestBasicExam(TestCase):

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


class TestComplexExam(TestCase):

    def setUp(self):

        self.MANUALS_QUAN = 3
        self.manuals = []

        self.SUBJECTS_QUAN = 13
        self.subjects = []

        self.questions = []
        self.QUESTIONS_QUAN = 151

        self.answers = []

        for i in range(self.MANUALS_QUAN):
            self.manuals.append(Manual.objects.create(manual='Manual%s' % i))

        for i in range(self.SUBJECTS_QUAN):
            self.subjects.append(Subject.objects.create(
                subject='Subject%s' % i,
                manual=self.manuals[(i % self.MANUALS_QUAN)]
                ))
        
        for i in range(self.QUESTIONS_QUAN):
            self.questions.append(Question.objects.create(
                subject=self.subjects[i%self.SUBJECTS_QUAN],
                question=u'Q%s' % i
                ))
            for j in range(4):
                self.answers.append(self.questions[i].answer_set.create(
                    answer=u'A%s%s' % (i,j),
                    is_correct=(j<2)
                    ))

        self.QUAN_QUESTIONS = 101
        self.TM = TestModel.objects.create(questions=self.QUAN_QUESTIONS)

        for i in range(self.SUBJECTS_QUAN):
            self.TM.testmodelsubject_set.create(
                subject=self.subjects[i],
                weight_from=6,
                weight_to=8
                )

        self.TEST_ITERATIONS = 2

    def test_create_random_test_questions(self):

        for i in range(self.TEST_ITERATIONS):

            T = self.TM.create_test()

            questions = T.create_random_test_questions(
                self.subjects[0].testmodelsubject_set.first(),11)

            self.assertEqual(len(questions),11)

    def test_random_weights(self):

        for i in range(self.TEST_ITERATIONS):
            tms_weights, total_weight = self.TM.random_weights()

            self.assertGreaterEqual(total_weight,6*self.SUBJECTS_QUAN)
            self.assertLessEqual(total_weight,8*self.SUBJECTS_QUAN)
            self.assertEqual(len(tms_weights),13)

            for (tms, w) in tms_weights:
                self.assertGreaterEqual(w,tms.weight_from)
                self.assertLessEqual(w,tms.weight_to)

    def test_exam_test(self):

        for i in range(self.TEST_ITERATIONS):
            T = self.TM.create_test()

            self.assertEqual(T.testquestion_set.count(), self.QUAN_QUESTIONS)

            valid_questions = ( ((i+1)*11) % self.QUAN_QUESTIONS ) + 1
            for tq in T.testquestion_set.all().order_by('?')[:valid_questions]:
                for ta in tq.testanswer_set.all()[:2]:
                    ta.is_correct = True
                    ta.save()

            note = T.get_test_note()

            self.assertEqual(note, float(valid_questions)/self.QUAN_QUESTIONS)


