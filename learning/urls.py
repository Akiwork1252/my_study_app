from django.urls import path
from . import views

app_name = 'learning'
urlpatterns = [
    path('lecture/<int:learning_plan_id>/', views.LectureChatView.as_view(), name='lecture_chat'),
]
