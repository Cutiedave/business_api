# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ABDD_rest.settings")
app = Celery("ABDD_rest", broker="redis://default:bLVoXmvY0aulFkAc5i30@containers-us-west-35.railway.app:7756")
#app.config_from_object("django.conf:settings")
app.autodiscover_tasks()