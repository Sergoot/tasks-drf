from DRF_APP_TEST.celery import app
from .services import notice_deadline_tasks


@app.task
def notice_deadline():
    notice_deadline_tasks()
