from time import sleep
from celery import shared_task

@shared_task
def notify_customers(massage):
    print('send 10k emails')
    print(massage)
    sleep(5)
    print('send shod')