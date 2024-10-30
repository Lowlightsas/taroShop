from django.shortcuts import render,redirect,reverse,get_object_or_404
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .tasks import share  # Импортируйте вашу задачу Celery

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
                        reverse('payment:canceled'))
        # данные сеанса Stripe оформления платежа
        session_data = {
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # добавить товарные позиции заказа
        # в сеанс оформления платежа Stripe
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
             'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        # создать сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        # перенаправит к платежной форме Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

def payment_completed(request):
    order_id = request.session.get('order_id')  # Get order_id from session

    if order_id:
        share.delay(order_id)  # Call Celery task to send email
        del request.session['order_id']  # Clear order_id from session after processing
    else:
        return render(request, 'payment/canceled.html')  # Handle the case where order_id is missing

    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request,'payment/canceled.html')