from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Валидатор проверяет является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsActive(permissions.BasePermission):
    """Валидатор для проверки поля пользователя is_active."""

    message = "Вы не являетесь активным пользователем."

    def has_permission(self, request, view):

        return request.user.is_active
