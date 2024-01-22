from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Права доступа только активным сотрудникам.
    """
    def has_permission(self, request, view):
        return request.user.is_active
