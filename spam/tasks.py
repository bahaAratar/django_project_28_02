from django.core.mail import send_mail
from celery import shared_task
from .models import Contact

@shared_task
def send_spam():
    emails = [i.email for i in Contact.objects.all()]
    send_mail(
        'activaion account', # title
        f'привет, загляни на наш сайт', # body
        'dead.baha.31@gmail.com', # from
        emails # to
    )