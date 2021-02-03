from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Admin':
            return True
        return False

class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Engineer'
