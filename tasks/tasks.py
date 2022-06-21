from celery.schedules import crontab

from DRF_APP_TEST.celery import app
from .services import mail, notice_deadline_tasks


@app.task
def send_notice(email, data):
    mail(email, data)


@app.task
def notice_deadline():
    notice_deadline_tasks()

