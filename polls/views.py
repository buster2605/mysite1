from django.shortcuts import render
from django.http import HttpResponse, Http404
from polls.models import Question
from django.template import RequestContext, loader

# Create your views here.

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = RequestContext(request, {
		'latest_question_list': latest_question_list,
		})
	return HttpResponse(template.render(context))

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
	response = "you are looking at the result of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("you are voting on question %s." %question_id)
