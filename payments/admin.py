from django.contrib import admin
from .models import Item, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Администратор для модели Item, который отображает имя, цену и описание.
    """
    list_display = ['name', 'price', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Администратор для модели Order отображает идентификатор,
    дату создания, общую сумму и статус.
    """
    list_display = ['id', 'created_at', 'total_amount', 'status']
    list_filter = ['status', 'created_at']
    filter_horizontal = ['items']
    readonly_fields = ['created_at']

    def save_model(self, request, obj, form, change):
        """
        Сохранение модели заказа и вычисление общей суммы.
        """
        super().save_model(request, obj, form, change)
        obj.calculate_total()



