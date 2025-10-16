from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для регистрации User в админке."""

    exclude = ("password",)
    list_filter = ('id', 'email', 'username', 'phone')
