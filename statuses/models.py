from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статусы'
        verbose_name_plural = 'Статусы'
        ordering = ['time_create', 'name']
