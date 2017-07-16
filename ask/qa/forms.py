from django import forms
from django.contrib.auth.models import User
from .models import Question, Answer
from django.core.exceptions import ObjectDoesNotExist

class AskForm(forms.Form):
	title = forms.CharField(max_length=200)
	text = forms.CharField(widget=forms.Textarea)
	#author = forms.IntegerField(required=True)
		
	def clean_title(self):
		title = self.cleaned_data['title']
		if title == None:
			raise forms.ValidationError(u"Title shouldn't be empty")
		return title
	
	def clean_text(self):
		text = self.cleaned_data['text']
		if text == None:
			raise forms.ValidationError(u"Text shouldn't be empty")
		return text
		
	def clean_author(self):
		return None
	
	def save(self):
		self.cleaned_data['author'] = self._author
		question = Question(**self.cleaned_data)
		question.save()
		return question

class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput)
	#author = forms.IntegerField(initial=1, required=False)
	
	#def __init__(self, question_id, post=None):
		#self.question_id = question_id
		#super(AnswerForm, self).__init__(post)
	
	def clean_text(self):
		text = self.cleaned_data['text']
		if text == "":
			raise forms.ValidationError(u"Text shouldn't be empty")
		return text
		
	def clean_author(self):
		return None
	
	#def clean_question(self):
		#try:
			#self.cleaned_data['question'] = int(self.cleaned_data['question'])
		#except ValueError:
			#raise forms.ValidationError(u"Question field must be numeric")
		
		#try:
			#self.cleaned_data['question'] = Question.objects.get(pk=self.cleaned_data['question'])
		#except Question.DoesNotExist:
			#raise forms.ValidationError(u"There is no such question")
	
	def save(self):
		self.cleaned_data['question'] = Question.objects.get(pk=self.cleaned_data['question'])
		self.cleaned_data['author'] = self._author
		answer = Answer(**self.cleaned_data)
		answer.save()
		return answer

class SignUpForm(forms.Form):
	username = forms.CharField(max_length=50, label="Username")
	email = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)
	
	def clean(self):
		try:
			user = User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data
		
		raise forms.ValidationError(u"Such user exists!")
			
	
	def save(self):
		user = User.objects.create_user(**self.cleaned_data)
		return user

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
