from celery import shared_task
from rest_framework.response import Response

@shared_task
def big_func():
    import time
    time.sleep(5)