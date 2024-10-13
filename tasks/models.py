from django.db import models
from users.models import User
from statuses.models import Status
from labels.models import Label


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=False, related_name="tasks_as_author",
                               verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="tasks_as_executor",
                                 verbose_name='Исполнитель')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    labels = models.ManyToManyField(Label, blank=True, verbose_name='Метки')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['pk']
