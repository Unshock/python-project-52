from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User


class Status(models.Model):

    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date"))
    name = models.CharField(
        max_length=100, verbose_name=_("Name"), unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_defalut_status(self):
        return Status.objects.get(name=_("New")).id

    def get_absolute_url(self):
        return reverse('create_status')

    def get_update_url(self):
        return reverse('update_status', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_status', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['creation_date', 'name']
