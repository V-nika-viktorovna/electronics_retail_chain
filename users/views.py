from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsActive, IsModer
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Класс настройки CRUD для модели User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """Метод для проверки доступа к функцианалу сайта, в зависимости от роли Пользователя."""

        if self.action in ["retrieve", "list"]:
            self.permission_classes = (IsActive,)
        elif self.action in ["create", "destroy", "partial_update", "update"]:
            self.permission_classes = (IsModer,)

        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод запускается, когда создается новый объект.
        Сначала сохраняем объект пользователя, устанавливая флаг активности (is_active=True).
        Затем пароль пользователя шифруется и пользователь сохраняется в базу данных"""

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):

        user = serializer.save()
        user.set_password(user.password)
        user.save()
