# django_celery/celery.py

import os
from celery import Celery

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ABDD_rest.settings")
app = Celery("ABDD_rest", broker_url="redis://default:bLVoXmvY0aulFkAc5i30@containers-us-west-35.railway.app:7756/1")
#app.config_from_object("django.conf:settings")
app.conf.update(
     CELERY_ACCEPT_CONTENT = ['json'],
     CELERY_TASK_SERIALIZER = 'json',
     CELERY_RESULT_SERIALIZER = 'json', 
)
app.autodiscover_tasks()