"""URL configuration for cloudhire_project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/resumes/', include('resumes.urls')),
    path('api/applications/', include('applications.urls')),
] + static('/media/', document_root=settings.BASE_DIR / 'media')
