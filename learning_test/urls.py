from django.urls import path

from . import views

urlpatterns = [
    path('learning_test/<int:learning_goal_id>', views.Test.as_view(), name='learning_test')
]
