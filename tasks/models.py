from django.db import models
from django.urls import reverse
from users.models import User
from statuses.models import Status


# Create your models here.
class Task(models.Model):
    taskname = models.CharField(max_length=50, unique=True, verbose_name='Задача')
    taskdescription = models.TextField(blank=True, null=True, verbose_name='Описание')
    taskautor = models.CharField(max_length=50, verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 verbose_name='Исполнитель')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        return reverse('task_info', kwargs={'pk': self.pk})

    def get_absolute_url_edit(self):
        return reverse('task_edit', kwargs={'pk': self.pk})

    def get_absolute_url_delete(self):
        return reverse('task_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.taskname

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['taskname']
