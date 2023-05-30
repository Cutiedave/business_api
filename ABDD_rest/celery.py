# django_celery/celery.py

import os
import psutil
from celery import Celery

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ABDD_rest.settings")
app = Celery("ABDD_rest", broker_url="redis://default:bLVoXmvY0aulFkAc5i30@containers-us-west-35.railway.app:7756/1")
#app.config_from_object("django.conf:settings")
app.conf.worker_max_tasks_per_child = 100

celery_max_mem_kilobytes = (psutil.virtual_memory().total * 0.4) / 1024

app.conf.worker_concurrency=1

app.conf.worker_max_memory_per_child = int(celery_max_mem_kilobytes / app.conf.worker_concurrency)

app.autodiscover_tasks()