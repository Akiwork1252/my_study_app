from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ascension.urls')),
    path('accounts/', include('allauth.urls')),
    path('ai_support/', include('ai_support.urls')),
]
