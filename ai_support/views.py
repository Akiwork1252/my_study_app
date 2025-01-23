from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from ascension.models import LearningGoal, LearningPlan
from .services import generate_learning_plan


# Create your views here.
class GenerateLearningPlanPreviewView(LoginRequiredMixin, View):
    def get(self, request, learning_goal_id):
        learning_goal = get_object_or_404(LearningGoal, id=learning_goal_id, 
                                          user=request.user)

        generated_plan = generate_learning_plan(
            title=learning_goal.title,
            current_level=learning_goal.current_level,
            description=learning_goal.description,
        )
        return render(request, 'ai_support/preview_learning_plan.html', 
                      {'generated_plan': generated_plan,
                       'learning_goal': learning_goal,
                       'learning_goal_id': learning_goal_id,
                       })

