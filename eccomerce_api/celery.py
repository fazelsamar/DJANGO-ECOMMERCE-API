import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eccomerce_api.settings')

celery = Celery('eccomerce_api')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()