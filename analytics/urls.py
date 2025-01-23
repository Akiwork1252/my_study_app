from django.urls import path
from . import views

app_name = 'analytics'
urlpatterns = [
    path('make_graph/<int:learning_goal_id>', views.make_graph, name='make_graph'),
]
