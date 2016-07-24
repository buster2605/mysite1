from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from polls.models import Question, Choice, Voter
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django import forms
from polls.forms import *
from django.template import RequestContext
from django.shortcuts import render, render_to_response

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
	if Voter.objects.filter(question_id=question_id, user_id=request.user.id).exists():
		return render(request, 'polls/detail.html',{
			'question':p,
			'error_message': 'you have already voted'
			})
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
		v = Voter(user = request.user, question=p)
		v.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/login')

class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(label='Password',
				widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password(Again)',
				widget=forms.PasswordInput())

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['password1'] == form.cleaned_data['password2']:
				user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
				return HttpResponseRedirect('/polls')
			else:
				form = RegistrationForm()
				return render(request, 'registration/register.html', {'error_message':'you have entered incorrect password', 'form':form})
	form = RegistrationForm()
	variables = RequestContext(request,{'form':form})
	return render_to_response('registration/register.html', variables)

# def base_page(generic.ListView):
# 	return HttpResponseRedirect('template/registration/base.html')
