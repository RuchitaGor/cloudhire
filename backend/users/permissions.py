"""Custom permissions for the users app."""

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to admin role users."""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsRecruiter(BasePermission):
    """Allow access only to recruiter role users."""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'recruiter'
        )


class IsCandidate(BasePermission):
    """Allow access only to candidate role users."""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'candidate'
        )
