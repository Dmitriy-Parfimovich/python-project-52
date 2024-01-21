from django.db import models
from django.contrib.auth.models import UserManager
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=20)
    time_create = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def get_absolute_url_edit(self):
        return reverse('user_edit', kwargs={'pk': self.pk})

    def get_absolute_url_delete(self):
        return reverse('user_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
