from django.db import models
from django.urls import reverse


class Label(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    name = models.CharField(
        max_length=100, verbose_name="Имя метки", unique=True)

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse('update_label', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('delete_label', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"
        ordering = ['creation_date', 'name']
