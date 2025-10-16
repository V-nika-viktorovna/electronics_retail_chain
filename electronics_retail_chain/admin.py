from django.contrib import admin

from .models import NetworkLink, Product


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'city']
    search_fields = ['name', 'city']
    actions = ["clear_debt"]

    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt_to_supplier=0)
        self.message_user(request, f'Задолженности сброшены у {updated_count} элементов.')

    clear_debt.short_description = "Обнулить долг"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date', 'created_by']
