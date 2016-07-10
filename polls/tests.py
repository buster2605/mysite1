from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone
from polls.models import Question

class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)
	
	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	#create a question with 'question_text' publish the number of days offset to now(-ve for past and +ve for future questions)
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text,
					pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		#if no question exists an appropriate message shoul be displayed
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
	
	def test_index_view_with_a_future_question(self):
		#question with pub_date in the future should be shown in index page
		create_question(question_text='Future Question', days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response,'No polls are available',
					status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_a_past_question(self):
		#question with pub_date in the future should be shown in index page
		create_question(question_text='Past Question', days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
				response.context['latest_question_list'],
				['<Question: Past Question>']
				)

	def test_index_view_with_future_question_and_past_question(self):
		#even if both future and past question exists only past questions will be displayed
		create_question(question_text="Past question", days=-30)
		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
				response.context['latest_question_list'],
				['<Question: Past question>']
				)

	def test_index_view_with_two_past_questions(self):
		create_question(question_text="Past Question 1.", days=-30)
		create_question(question_text="Past Question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
				response.context['latest_question_list'],
				['<Question: Past Question 2.>','<Question: Past Question 1.>']
				)

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		#the detail view of the question with a pub_date in the future should return a 404 not found
		future_question = create_question(question_text='Future question.',
						days=5)
		response = self.client.get(reverse('polls:detail',
					args=(future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		#the detail view with the questio with the pub_date in the past should display the question's text
		past_question = create_question(question_text='Past question.',
						days=-5)
		response = self.client.get(reverse('polls:detail',
					args=(past_question.id,)))
		self.assertContains(response, past_question.question_text,
				status_code=200)
