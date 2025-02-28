import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

"""
Этот модуль содержит представления для обработки покупок и оформления заказов в интернет-магазине.
Импортируются необходимые библиотеки и модели:
- stripe: для интеграции с платежной системой Stripe.
- settings: для доступа к настройкам проекта.
- get_object_or_404, render, redirect: для обработки HTTP-запросов и ответов.
- JsonResponse: для возврата JSON-ответов.
"""

def home(request):
    """
    Отображает главную страницу с доступными товарами.
    """
    items = Item.objects.all()
    return render(request, 'home.html', {
        'items': items
    })



def item_detail(request, id):
    """
    Отображает подробную информацию о конкретном товаре по его идентификатору.
    """
    item = get_object_or_404(Item, id=id)
    return render(request, 'item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def create_checkout_session(request, id):
    """
    Создает сессию оформления заказа в Stripe для выбранного товара и возвращает идентификатор сессии.
    """
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/item/{id}/'),
        cancel_url=request.build_absolute_uri(f'/item/{id}/'),
    )

    return JsonResponse({'id': session.id})



def order_create(request):
    """
    Обрабатывает создание нового заказа. Принимает список идентификаторов товаров и создает заказ.
    """
    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        if item_ids:
            order = Order.objects.create()
            order.items.set(item_ids)
            order.calculate_total()
            return redirect('order-detail', order_id=order.id)

    items = Item.objects.all()
    return render(request, 'order_create.html', {'items': items})


def order_detail(request, order_id):
    """
    Отображает детали заказа по его идентификатору.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def create_order_checkout_session(request, order_id):
    """
    Создает сессию оформления заказа в Stripe для всех товаров в заказе и возвращает идентификатор сессии.
    """
    order = get_object_or_404(Order, id=order_id)

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.name,
                'description': item.description,
            },
            'unit_amount': item.price,
        },
        'quantity': 1,
    } for item in order.items.all()]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(f'/order/{order_id}/success/'),  # Обновляем URL
        cancel_url=request.build_absolute_uri(f'/order/{order_id}/'),
    )

    return JsonResponse({'id': session.id})


def order_success(request, order_id):
    """
    Обрабатывает успешное завершение заказа, обновляет статус заказа на 'PAID'
    и отображает страницу с подтверждением заказа.
    """
    order = get_object_or_404(Order, id=order_id)
    order.status = 'PAID'
    order.save()
    return render(request, 'order_success.html', {'order': order})




