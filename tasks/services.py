from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.db.models.base import Model
from django.db.models import QuerySet
from DRF_APP_TEST import settings


def mail(email: str, data: dict) -> None:
    """ Отправляет на почту напоминание о дедлайне по задаче """
    subject = f'НАПОМИНАНИЕ! Завтра наступает дедлайн задачи {data["title"]}'
    message = f'{data["body"]}\nДедлайн: {data["deadline"]}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)


def get_all_or_filter(model: Model, **filters: any) -> QuerySet:
    """ Возвращает QuerySet со всеми атрибутами модели или отфильтрованными по фильтрам атрибутами """
    return model.objects.filter(**filters) if filters else model.objects.all()


def get_notice_time(deadline: str) -> int:
    """ Возвращает время, через которое придет напоминание о дедлайне """
    print((datetime.strptime(deadline, "%Y-%m-%d") - datetime.today() - timedelta(days=1)).seconds)
    return (datetime.strptime(deadline, "%Y-%m-%d") - datetime.today() - timedelta(days=1)).seconds






