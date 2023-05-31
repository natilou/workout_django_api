from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_superuser:
            return True
        if request.method == "GET":
            return True
