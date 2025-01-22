from django.urls import path
from . import views

app_name = 'learning_test'
urlpatterns = [
    path('multiple_choice/<int:learning_goal_id>', views.choice_test_view, name='choice_test'),
    path('written_test/<int:learning_goal_id>', views.written_test_view, name='written_test'),
]
