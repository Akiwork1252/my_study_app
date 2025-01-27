from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from .import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('ascension.urls', 'ascension'), namespace='ascension')),
    path('accounts/', include('allauth.urls')),
    path('ai_support/', include(('ai_support.urls', 'ai_support'), namespace='ai_support')),
    path('learning/', include(('learning.urls', 'learning'), namespace='learning')),
    path('learning_test/', include(('learning_test.urls', 'learning_test'), namespace='learning_test')),
    path('analytics/', include(('analytics.urls', 'analytics'), namespace='analytics')),
]

urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)
