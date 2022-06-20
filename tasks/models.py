from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """ Модель Тэга """
    tag_name = models.SlugField('Тэг',blank=False, default='unnamed tag')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag', default='')

    def __str__(self):
        return self.tag_name


class Task(models.Model):
    """ Модель Задачи """
    title = models.CharField('Заголовок', db_index=True, max_length=64, blank=False)
    body = models.TextField('Описание', max_length=400, blank=False,)
    is_important = models.BooleanField('Важное', default=False)
    date_published = models.DateTimeField('Время создания', default=timezone.now)
    deadline = models.DateField('Дедлайн', blank=False, null=False, default=timezone.now,)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task', default='')
    is_completed = models.BooleanField('Завершено', default=False)

    def __str__(self):
        return f"{self.title} Дедлайн: {self.deadline}"
