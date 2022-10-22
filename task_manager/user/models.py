from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #username = models.CharField(max_length=50, name='username', unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    USERNAME_FIELD = 'username'

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_update_url(self):
        return reverse('update_user', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_user', kwargs={'pk': self.pk})

# class User1(models.Model):
#     objects = None
#     creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
#     first_name = models.CharField(max_length=100, null=False, verbose_name="Имя")
#     last_name = models.CharField(max_length=100, verbose_name="Фамилия")
#     username = models.CharField(max_length=100, verbose_name="Логин")
# 
#     USERNAME_FIELD = 'username'
# 
#     @property
#     def full_name(self):
#         return self.first_name + ' ' + self.last_name
# 
#     def __str__(self):
#         return self.full_name
# 
#     def get_absolute_url(self):
#         return reverse('create_user')
# 
#     def get_delete_url(self):
#         return reverse('delete_user', kwargs={'user_id': self.pk})
# 
#     def get_update_url(self):
#         return reverse('update_user', kwargs={'user_id': self.pk})
# 
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#         ordering = ['creation_date', 'username']