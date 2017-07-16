from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Question, Answer
from .forms import AskForm, AnswerForm, SignUpForm, LoginForm

def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question_details(request, question_id):
	
	user = None
	
	if request.user.is_authenticated():
		user = request.user
	
	q = get_object_or_404(Question, pk=question_id)
	
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():			
			form._author = user
			answer = form.save()
			return HttpResponseRedirect('/question/' + str(answer.question.id) + '/')
	else:
		form = AnswerForm(initial={'question': question_id})
			
	#answers = Answer.objects.filter(question__id=question_id)
	
	return render(request, 'qa/question_details.html', {
		'question': q, 
		'answers': q.answer_set.all(), 
		'form': form,
		'user': user
	})
	
def new_questions(request):
	
	new_questions = Question.objects.new()
	
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		page = 1
		
	limit = 10
		
	paginator = Paginator(new_questions, limit)	
	paginator.baseurl = '/?page=';
	
	try:
		page = paginator.page(page)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	
	return render(request, 'qa/new_questions.html',{
		'questions': page.object_list,
		'paginator': paginator,
		'page': page,
		})
	
def popular_questions(request):
	
	new_questions = Question.objects.popular()
	
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		page = 1
		
	limit = 10
		
	paginator = Paginator(new_questions, limit)
	paginator.baseurl = '/popular/?page=';
	
	try:
		page = paginator.page(page)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	
	return render(request, 'qa/popular_questions.html',{
		'questions': page.object_list,
		'paginator': paginator,
		'page': page
		})

@login_required(login_url='/login/')
def ask_form(request):
	
	if request.method == "POST":
		form = AskForm(request.POST)
		
		if form.is_valid():			
			form._author = request.user
			question = form.save()
			return HttpResponseRedirect('/question/' + str(question.id) + '/')
	else:
		form = AskForm()
	
	return render(request, 'qa/ask_form.html', {'form':form})

def signup(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():		
			user = form.save()	
			
			#user = authenticate(request, username=username, password=password)
		#login user after signing up
			if user is not None:
				login(request, user)
			
			return HttpResponseRedirect("/")
	else:
		form = SignUpForm()
	
	return render(request, "qa/signup.html", {'form': form})

def login_view(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	
	error = None
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			form = LoginForm()
			error = 'Login/password error'
	else:
		form = LoginForm()
	
	return render(request, 'qa/login_form.html', {'form': form, 'error': error})
	
def logout_view(request):
	logout(request)
	
	return HttpResponseRedirect('/login/')
