from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def share(order_id):
    try:
        print(f"Received order_id: {order_id}")  # Отладочное сообщение
        order = Order.objects.get(id=order_id)
        
        subject = f'My shop - Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'
        
        email = EmailMessage(subject, message, 'sultanaevaakbota@gmail.com', [order.email])
        
        html = render_to_string('orders/order/pdf.html', {'order': order})
        
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        
        email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
        
        email.send()
    
    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")