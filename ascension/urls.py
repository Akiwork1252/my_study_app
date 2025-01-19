from django.urls import path
from . import views


app_name = 'ascension'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('interest-list/', views.InterestListView.as_view(), name='interest_list'),
    path('learning-goal/category/<int:category_id>/', views.LearningGoalByCategoryView.as_view(), name='learning_goal_by_category'),
    path('add-interest-category/', views.AddInterestCategoryView.as_view(), name='add_interest_category'),
    path('learning-goal/<int:category_id>/create/', views.CreateLearningGoal.as_view(), name='create_learning_goal'),
    path('save-plan/<int:learning_goal_id>/', views.SaveSelectedLearningPlanView.as_view(), name='save_selected_plan'),
    path('learning-plan-list/<int:learning_goal_id>/', views.LearningPlanListView.as_view(), name='learning_plan_list'),
]
