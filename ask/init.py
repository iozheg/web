from qa.models import Question, Answer
from django.utils import timezone

q1 = Question(
	title = "One",
	text = "This is one?",
	added_at = timezone.now(),
	rating = 0
	
)
