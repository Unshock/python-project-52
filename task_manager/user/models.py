from django.db import models

# Create your models here.


class User(models.Model):
    objects = None
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
