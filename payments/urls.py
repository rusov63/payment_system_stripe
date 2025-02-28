from django.urls import path
from . import views

# URL конфигурация для приложения магазина.
# Этот модуль определяет шаблоны URL для приложения магазина, сопоставляя URL с соответствующими функциями представлений.

urlpatterns = [
    path('', views.home, name='home'), # домашней страница
    path('item/<int:id>/', views.item_detail, name='item-detail'), # Направляет на представление item_detail для отображения деталей
    path('buy/<int:id>/', views.create_checkout_session, name='create-checkout-session'),  # оформления заказа для покупки товара
    path('order/create/', views.order_create, name='order-create'), # Направляет на представление order_create для создания нового заказа
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),  # Направляет на представление order_detail для отображения деталей конкретного заказа

    # Инициирует сессию оформления заказа для существующего заказа
    path('order/<int:order_id>/checkout/', views.create_order_checkout_session, name='order-checkout'),

    # Отображает страницу успеха после успешного оформления заказа.
    path('order/<int:order_id>/success/', views.order_success, name='order-success'),
]

