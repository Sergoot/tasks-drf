from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.db.models.base import Model
from django.db.models import QuerySet
from django.forms import model_to_dict

from DRF_APP_TEST import settings
from tasks.models import Task


def mail(email: str, data: dict) -> None:
    """ Отправляет на почту напоминание о дедлайне по задаче """
    subject = f'НАПОМИНАНИЕ! Завтра наступает дедлайн задачи {data["title"]}'
    message = f'{data["body"]}\nДедлайн: {data["deadline"]}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)


def get_all_or_filter(model: Model, **filters: any) -> QuerySet:
    """ Возвращает QuerySet со всеми атрибутами модели или отфильтрованными по фильтрам атрибутами """
    return model.objects.filter(**filters) if filters else model.objects.all()



def queryset_filter(queryset: QuerySet, **filters: any) -> QuerySet:
    """ Возвращает фильтрованный QuerySet """
    return queryset.filter(**filters) if filters else queryset


def notice_deadline_tasks() -> None:
    """ Оповещает пользователя о приближении дедлайна по задаче """
    tasks = Task.objects.filter(is_completed=False)
    for task in tasks:
        if (datetime.strptime(str(task.deadline), "%Y-%m-%d") - datetime.today()).seconds < 86400:
            mail(task.user.email, model_to_dict(task))



