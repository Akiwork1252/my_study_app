from django.urls import path
from . import views


app_name = 'ascension'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryViwe.as_view(), name='inquiry'),
]

