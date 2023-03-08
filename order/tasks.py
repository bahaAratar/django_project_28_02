from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_order_confirmation_code(email, code, title, price):
    full_link = f'привет, подтверди заказ на продукт {title} на сумму {price}\n\nhttp://127.0.0.1:8000/order/confirm/{code}'
    send_mail(
        'order of shop py25',
        full_link,
        settings.EMAIL_HOST_USER,
        [email],
    )