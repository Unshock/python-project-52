from django.db import models
from django.urls import reverse

from task_manager.labels.models import Label
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
        verbose_name="Создатель", related_name='task_creator')
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name="Исполнитель", related_name='executor', null=True)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT,
        verbose_name="Назначенный статус")
    labels = models.ManyToManyField(
        Label,
        through='TasksLabels',
        through_fields=('task', 'label'),
        blank=True,
        related_name='tasks',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_task', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('update_task', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_task', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['creation_date', 'name']


class TasksLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             null=True,
                             )
    label = models.ForeignKey(Label, on_delete=models.PROTECT,
                              null=True,
                              )

    class Meta:
        verbose_name = "Метка задачи"
        verbose_name_plural = "Метки задач"
        ordering = ['task']



