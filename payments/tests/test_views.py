from django.test import TestCase, Client
from unittest.mock import patch
from payments.models import Item, Order


class ViewsTestCase(TestCase):
    def setUp(self):
        """
        Подготовка данных для тестов
        """
        self.client = Client()
        self.item = Item.objects.create(
            name="Тестовый товар",
            description="Описание тестового товара",
            price=1000
        )
        self.order = Order.objects.create()
        self.order.items.add(self.item)

        # Определяем URL-пути, которые используются в тестах
        self.home_url = '/'
        self.item_detail_url = f'/item/{self.item.id}/'
        self.checkout_session_url = f'/buy/{self.item.id}/'
        self.order_create_url = '/order/create/'
        self.order_detail_url = f'/order/{self.order.id}/'
        self.order_checkout_url = f'/order/{self.order.id}/checkout/'
        self.order_success_url = f'/order/{self.order.id}/success/'

    def test_home_view(self):
        """
        Тест главной страницы
        """
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('items', response.context)

    def test_item_detail_view(self):
        """
        Тест страницы деталей товара
        """
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item.html')
        self.assertEqual(response.context['item'], self.item)

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_stripe_create):
        """
        Тест создания сессии оплаты для товара
        """
        mock_stripe_create.return_value.id = 'test_session_id'

        response = self.client.post(self.checkout_session_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'test_session_id')

    def test_order_create_get(self):
        """
        Тест GET-запроса страницы создания заказа
        """
        response = self.client.get(self.order_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_create.html')

    def test_order_create_post(self):
        """
        Тест POST-запроса создания заказа
        """
        response = self.client.post(self.order_create_url, {'items': [self.item.id]})
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertTrue(Order.objects.filter(items=self.item).exists())

    def test_order_detail_view(self):
        """
        Тест страницы деталей заказа
        """
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')
        self.assertEqual(response.context['order'], self.order)

    @patch('stripe.checkout.Session.create')
    def test_create_order_checkout_session(self, mock_stripe_create):
        """
        Тест создания сессии оплаты для заказа
        """
        mock_stripe_create.return_value.id = 'test_session_id'

        response = self.client.post(self.order_checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'test_session_id')

    def test_order_success_view(self):
        """
        Тест страницы успешного завершения заказа
        """
        response = self.client.get(self.order_success_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_success.html')

        # Проверяем, что статус заказа обновился
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'PAID')

    def test_item_detail_404(self):
        """
        Тест несуществующего товара
        """
        response = self.client.get(f'/item/999/')
        self.assertEqual(response.status_code, 404)

    def test_order_detail_404(self):
        """
        Тест несуществующего заказа
        """
        response = self.client.get(f'/order/999/')
        self.assertEqual(response.status_code, 404)
