from django.db import models

class Item(models.Model):
    """
    Представляет продукт, доступный для заказа.

    Атрибуты:
        name (str): Название товара, ограниченное 100 символами.
        description (str): Подробное описание товара.
        price (int): Цена товара в центах. По умолчанию 0.

    Методы:
        **str**(): Возвращает название товара в виде строки.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Order(models.Model):
    """
    Представляет заказ клиента, содержащий несколько товаров.

    Атрибуты:
        items (ManyToManyField): Связь многие ко многим с Item, позволяющая иметь несколько товаров в одном заказе.
        created_at (DateTimeField): Временная метка, когда заказ был создан, устанавливается автоматически при создании.
        total_amount (int): Общая сумма заказа. По умолчанию 0.
        status (str): Текущий статус заказа, который может быть 'PENDING' (в ожидании),
         'PAID' (оплачен) или 'CANCELLED' (отменён). По умолчанию 'PENDING'.

    Методы:
        **str**(): Возвращает строковое представление заказа, включая его ID.
        calculate_total(): Вычисляет и обновляет общую сумму заказа на основе выбранных товаров.
        save(*args, **kwargs): Переопределяет метод сохранения, чтобы вычислить общую сумму перед
        сохранением.
    """
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PAID', 'Paid'),
            ('CANCELLED', 'Cancelled')
        ],
        default='PENDING'
    )

    def __str__(self):
        return f"Order {self.id}"

    def calculate_total(self):
        total = sum(item.price for item in self.items.all())
        if self.total_amount != total:
            Order.objects.filter(id=self.id).update(total_amount=total)
            self.total_amount = total
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total()
