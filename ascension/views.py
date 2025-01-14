from django.views import generic
from django.shortcuts import render

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html'