from django.db import models
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.user.models import User


class Task(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    name = models.CharField(
        max_length=100, verbose_name="Имя задачи", unique=True)
    description = models.CharField(
        max_length=300, verbose_name="Описание задачи")
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="Создатель", related_name='creator')
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name="Исполнитель", related_name='executor', null=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET_DEFAULT,
        default='1',
        verbose_name="Назначенный статус"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('create_task')

    def get_detail_url(self):
        return reverse('detail_task', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('update_task', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_task', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['creation_date', 'name']
