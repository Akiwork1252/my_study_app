from django.urls import path
from . import views

app_name = 'analytics'
urlpatterns = [
    path('data_top_menu/<int:learning_goal_id>', views.DataTopView.as_view(), name='data_top_menu'),
    path('show_total_score_graph/<int:learning_goal_id>', views.show_total_score_graph, name='show_total_score_graph'),
    path('show_topic_test_score_graph/<int:learning_goal_id>', views.show_topic_score_graph, name='show_topic_test_score_graph'),
]
