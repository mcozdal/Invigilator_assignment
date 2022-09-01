from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .assign import assign
# BROKER_URL = 'redis://localhost:6379/0'
# app = Celery('tasks', broker=BROKER_URL)


@shared_task
def task1(excel_path):
    try:
        if assign(excel_path):
            return True
    except Exception as e:
        print(e)
