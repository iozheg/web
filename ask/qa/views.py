from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from .models import Question, Answer

def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question_details(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	answers = Answer.objects.filter(question__id=question_id)
	
	return render(request, 'qa/question_details.html', {'question': q, 'answers': answers})
	
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

def create_test_questions():
	q = Question(title="first")
