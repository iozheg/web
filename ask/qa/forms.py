from django import forms
from .models import Question, Answer
from django.core.exceptions import ObjectDoesNotExist

class AskForm(forms.Form):
	title = forms.CharField(max_length=200)
	text = forms.CharField(widget=forms.Textarea)
	
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
	
	def save(self):
		question = Question(title = self.cleaned_data['title'], text = self.cleaned_data['text'])
		question.save()
		return question

class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	#question = forms.CharField(max_length=30)
	
	def __init__(self, question_id, post=None):
		self.question_id = question_id
		super(AnswerForm, self).__init__(post)
	
	def clean_text(self):
		text = self.cleaned_data['text']
		if text == "":
			raise forms.ValidationError(u"Text shouldn't be empty")
		return text
	
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
		self.cleaned_data['question'] = Question.objects.get(pk=self.question_id)
		answer = Answer(**self.cleaned_data)
		answer.save()
		return answer
