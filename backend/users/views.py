"""Views for the users app."""

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdmin

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user (candidate or recruiter)."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomLoginView(TokenObtainPairView):
    """Login endpoint that returns JWT tokens + user info."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    """Return the currently authenticated user's profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AdminUserListView(generics.ListAPIView):
    """Admin: list all users."""
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by('-date_joined')


class AdminUserDeleteView(generics.DestroyAPIView):
    """Admin: delete a user."""
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
