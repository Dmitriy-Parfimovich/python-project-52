from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def get_absolute_url_edit(self):
        return reverse('user_edit', kwargs={'pk': self.pk})

    def get_absolute_url_delete(self):
        return reverse('user_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['time_create', 'username']
