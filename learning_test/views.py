from django.shortcuts import render
from django.views import generic

from ai_support.services import generate_multiple_choice_questions, generate_coding_questions 
from ascension.models import LearningPlan
from analytics.models import Progress


# Create your views here.
class Test(generic.TemplateView):
    template_name = 'learning_test/test.html'