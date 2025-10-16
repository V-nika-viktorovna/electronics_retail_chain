from django.db import models

from users.models import User

NULFLAG = {"blank": True, "null": True}


class Product(models.Model):
    """Класс модели продукта."""

    name = models.CharField(max_length=255, verbose_name='Название продукта',
                            help_text='Название продукта')

    model = models.CharField(max_length=100, verbose_name='Модель',
                             **NULFLAG, help_text='Модель')

    release_date = models.DateField(verbose_name='дата выхода продукта на рынок',
                                    **NULFLAG, help_text='дата выхода продукта на рынок')

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, **NULFLAG,
                                   verbose_name='Создавший пользователь', help_text='Создавший пользователь')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name}, {self.model}"


class NetworkLink(models.Model):
    """Основная модель, хранит поставщиков всех уровней сети."""

    LEVEL_CHOICES = [
        ('Завод', 'Завод'),
        ('Розничная сеть', 'Розничная сеть'),
        ('Индивидуальный предприниматель', 'Индивидуальный предприниматель')
    ]

    name = models.CharField(max_length=255, verbose_name="Название",
                            help_text="Название")

    email = models.EmailField(verbose_name="Email", help_text="email", **NULFLAG)

    country = models.CharField(max_length=100, verbose_name="Страна",
                               help_text="Введите назание страны", **NULFLAG)

    city = models.CharField(max_length=100, verbose_name="Город",
                            help_text="Введите назание города", **NULFLAG)

    street = models.CharField(max_length=100, verbose_name="Улица",
                              help_text="Введите назание улицы", **NULFLAG)

    house_number = models.PositiveIntegerField(verbose_name="Номер дома",
                                               help_text="Введите номер дома", **NULFLAG)

    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name="Уровень доступа",
                             help_text="Уровень доступа")

    products = models.ManyToManyField(Product, **NULFLAG)

    supplier = models.ForeignKey('NetworkLink', on_delete=models.SET_NULL, verbose_name="Поставщик",
                                 help_text="Поставщик", **NULFLAG)

    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="Долг перед поставщиком",
                                           help_text="Долг перед поставщиком", **NULFLAG)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, **NULFLAG,
                                   verbose_name='Создавший пользователь', help_text='Создавший пользователь')

    # def save(self, *args, **kwargs):
    #     if not self.supplier:  # если поставщик не указан
    #         self.supplier = self  # устанавливаем ссылку на себя
    #     super(NetworkLink, self).save(*args, **kwargs)

    class Meta:
        ordering = ["city"]
        verbose_name = "Звено сети"
        verbose_name_plural = "Звено сети"

    def __str__(self):
        return self.name
