#encoding=utf-8
from __future__ import absolute_import
from celery import Celery
app = Celery('task', include=['task.tasks'])
app.config_from_object('task.celeryconfig')
if __name__ == '__main__':
    app.start()
