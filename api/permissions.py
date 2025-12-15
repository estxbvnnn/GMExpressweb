from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """Allow read-only for everyone, write only for staff/superusers."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class IsOwnerOrStaff(permissions.BasePermission):
    """Allow owners to manage their objects; staff/superusers can manage all."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return True
            return getattr(obj, "user", None) == request.user
        return False
