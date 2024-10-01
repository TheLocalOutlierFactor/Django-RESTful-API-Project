from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInGroup(BasePermission):
    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name=self.group_name).exists()
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
