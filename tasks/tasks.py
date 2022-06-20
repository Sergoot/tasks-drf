from DRF_APP_TEST.celery import app
from .services import mail


@app.task
def send_notice(email, data):
    mail(email, data)
