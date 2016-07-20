from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from polls.models import Question, Choice
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Create your views here.
class IndexView(generic.ListView):
    login_required = True
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.(not including those set to be published in the future)"""
        return Question.objects.filter(
		pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]
 
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super(IndexView, self).dispatch(*args, **kwargs)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        #excludes any questions that are not published yet
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the question voying form
		return render(request, 'polls/detail.html',{
			'question':p,
			'error_message':"You didn't select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
