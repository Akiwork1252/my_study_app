from django.urls import path
from . import views

app_name = 'ai_support'
urlpatterns = [
    path('generate/preview/<int:learning_goal_id>/', 
         views.GenerateLearningPlanPreviewView.as_view(), 
         name='generate_plan_preview'),
]
