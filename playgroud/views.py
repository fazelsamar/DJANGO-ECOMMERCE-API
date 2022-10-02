from django.shortcuts import render
from .tasks import notify_customers

def hello(r):
    notify_customers.delay('hello')
    return render(r, 'playground/index.html')