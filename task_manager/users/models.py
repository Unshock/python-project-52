from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date"))
    USERNAME_FIELD = 'username'

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    # To delete
    # def get_update_url(self):
    #     return reverse('update_user', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('delete_user', kwargs={'pk': self.pk})
