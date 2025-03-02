from django.test import TestCase
from django.core.exceptions import ValidationError
from payments.models import Item, Order

class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            price=1000
        )

    def test_item_creation(self):
        """Тест создания объекта Item"""
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.description, "Test Description")
        self.assertEqual(self.item.price, 1000)

    def test_item_str_representation(self):
        """Тест строкового представления объекта Item"""
        self.assertEqual(str(self.item), "Test Item")

    def test_get_display_price(self):
        """Тест метода форматирования цены"""
        self.assertEqual(self.item.get_display_price(), "10.00")

    def test_empty_name_validation(self):
        """Тест валидации пустого имени"""
        item = Item(name="", description="Test", price=100)
        with self.assertRaises(ValidationError):
            item.full_clean()

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create()
        self.item1 = Item.objects.create(name="Item 1", price=1000)
        self.item2 = Item.objects.create(name="Item 2", price=2000)

    def test_order_creation(self):
        """Тест создания объекта Order"""
        self.assertEqual(self.order.status, 'PENDING')
        self.assertEqual(self.order.total_amount, 0)

    def test_order_str_representation(self):
        """Тест строкового представления объекта Order"""
        self.assertEqual(str(self.order), f"Order {self.order.id}")

    def test_calculate_total(self):
        """Тест расчета общей суммы заказа"""
        self.order.items.add(self.item1, self.item2)
        self.order.calculate_total()
        self.assertEqual(self.order.total_amount, 3000)

    def test_status_choices(self):
        """Тест выбора статуса заказа"""
        self.order.status = 'PAID'
        self.order.save()
        self.assertEqual(self.order.status, 'PAID')

        # Проверка недопустимого статуса
        with self.assertRaises(ValidationError):
            self.order.status = 'INVALID_STATUS'
            self.order.full_clean()



# python manage.py test payments