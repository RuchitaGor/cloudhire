"""URL patterns for the users app."""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, CustomLoginView, MeView, AdminUserListView, AdminUserDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-users-list'),
    path('admin/users/<int:pk>/', AdminUserDeleteView.as_view(), name='admin-users-delete'),
]
