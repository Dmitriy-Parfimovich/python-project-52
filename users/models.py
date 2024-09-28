from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.
class User(AbstractUser, PermissionsMixin):

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['time_create', 'username']
