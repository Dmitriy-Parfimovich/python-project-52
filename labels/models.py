from django.db import models
from django.urls import reverse


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    """def get_absolute_url_edit(self):
        return reverse('label_edit', kwargs={'pk': self.pk})

    def get_absolute_url_delete(self):
        return reverse('label_delete', kwargs={'pk': self.pk})"""

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метки'
        verbose_name_plural = 'Метки'
        ordering = ['time_create', 'name']
