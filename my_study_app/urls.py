from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('ascension.urls', 'ascension'), namespace='ascension')),
    path('accounts/', include('allauth.urls')),
    path('ai_support/', include(('ai_support.urls', 'ai_support'), namespace='ai_support')),
    path('learning/', include(('learning.urls', 'learning'), namespace='learning')),
    path('learning_test/', include(('learning_test.urls', 'learning_test'), namespace='learning_test')),
]
