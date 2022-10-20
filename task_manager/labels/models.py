from django.db import models
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.user.models import User



class Label(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    name = models.CharField(
        max_length=100, verbose_name="Имя метки", unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="Создатель", related_name='labels')



    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('create_label')

    def get_update_url(self):
        return reverse('update_label', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_label', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"
        ordering = ['creation_date', 'name']
