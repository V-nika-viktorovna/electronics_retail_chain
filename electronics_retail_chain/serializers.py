from rest_framework import serializers
from .models import NetworkLink, Product


class ProductSerializer(serializers.ModelSerializer):
    """Класс сериализатора для модели Product."""

    class Meta:
        model = Product
        fields = '__all__'


class NetworkLinkSerializer(serializers.ModelSerializer):
    """Класс сериализатора для модели NetworkLink."""

    products = ProductSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        """Метод защиты от прямого редактирования поля debt_to_supplier через API."""

        if 'debt_to_supplier' in validated_data:
            raise serializers.ValidationError("Обновление поля 'задолженности' запрещено.")
        return super().update(instance, validated_data)

    class Meta:
        model = NetworkLink
        fields = "__all__"
        extra_kwargs = {
            'supplier': {'required': False}
        }


class NetworkLinkDetailSerializer(serializers.ModelSerializer):
    """Детальной информации по одному объекту модели NetworkLink."""

    products = ProductSerializer(many=True, read_only=True)
    count_products = serializers.SerializerMethodField()
    url_supplier = serializers.SerializerMethodField()
    hierarchy = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        """Метод защиты от прямого редактирования поля debt_to_supplier через API."""

        if 'debt_to_supplier' in validated_data:
            raise serializers.ValidationError("Обновление поля 'задолженности' запрещено.")
        return super().update(instance, validated_data)

    def get_count_products(self, obj):
        """Метод для получения количества продуктов поставщика."""

        #return Lesson.objects.filter(name=course).count()

        return obj.products.count()

    def get_url_supplier(self, obj):
        """Метод для получения ссылки на поставщика."""
        supplier = obj.supplier
        url_supplier = f"http://127.0.0.1:8000/electronics_retail_chain/networklink/{supplier.pk}/"
        return url_supplier

    def get_hierarchy(self, obj):
        if "Завод" in obj.level:
            hierarchy = 0
        elif obj.pk == obj.supplier.pk:
            hierarchy = 0
        else:
            hierarchy = 1
        return hierarchy

    class Meta:
        model = NetworkLink
        fields = "__all__"
