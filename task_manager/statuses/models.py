from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):

    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date"))
    name = models.CharField(
        max_length=100, verbose_name=_("Name"), unique=True)

    def __str__(self):
        return self.name

    # To delete
    # def get_update_url(self):
    #     return reverse('update_status', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('delete_status', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['creation_date', 'name']
