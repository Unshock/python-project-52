from django.db import models
from django.urls import reverse

from task_manager.user.models import User


class Status(models.Model):
    #objects = None
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    name = models.CharField(
        max_length=100, verbose_name="Имя статуса", unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_defalut_status(self):
        return Status.objects.get(name="Новый").id

    def get_absolute_url(self):
        return reverse('create_status')

    def get_update_url(self):
        return reverse('update_status', kwargs={'status_id': self.pk})

    def get_delete_url(self):
        return reverse('delete_status', kwargs={'status_id': self.pk})

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['creation_date', 'name']
