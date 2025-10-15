from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from electronics_retail_chain.models import NetworkLink, Product
from electronics_retail_chain.serializers import (NetworkLinkDetailSerializer,
                                 NetworkLinkSerializer, ProductSerializer)
from users.permissions import IsModer, IsActive


class ProductViewSet(ModelViewSet):
    """Класс настройки CRUD для модели Product."""

    serializer_class = ProductSerializer
    # Получаем все данне из БД
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        """Метод вызывается при создании нового объекта.
        Присваувает значение пол. created_by равным текущему авторизованному пользователю."""

        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        """Проверка прав доступа в зависимости от роли пользователя."""

        if self.action in ["retrieve", "list"]:
            self.permission_classes = (IsActive,)
        elif self.action in ["create", "destroy", "partial_update", "update"]:
            self.permission_classes = (IsModer,)

        return super().get_permissions()


class NetworkLinkViewSet(ModelViewSet):
    """Класс настройки CRUD для модели NetworkLink."""

    serializer_class = NetworkLinkSerializer
    queryset = NetworkLink.objects.all()
    filterset_fields = ("country",)

    def perform_create(self, serializer):
        """Метод вызывается при создании нового объекта.
        Присваувает значение пол. created_by равным текущему авторизованному пользователю."""
        #
        # networklink = serializer.save()
        # networklink.created_by = self.request.user
        # networklink.save()

        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        """Метод позволяющий определить сериализатор для вывода всего списка
        или просмотра детальной информации."""

        if self.action == "retrieve":
            return NetworkLinkDetailSerializer

        return NetworkLinkSerializer

    def get_permissions(self):
        """Метод для проверки доступа к функцианалу сайта, в зависимости от роли Пользователя."""

        if self.action in ["retrieve", "list"]:
            self.permission_classes = (IsActive,)
        elif self.action in ["create", "destroy", "partial_update", "update"]:
            self.permission_classes = (IsModer,)

        return super().get_permissions()

    def get_queryset(self):
        queryset = NetworkLink.objects.all()
        country_filter = self.request.query_params.get('country', None)
        if country_filter is not None:
            queryset = queryset.filter(country=country_filter)
        return queryset
