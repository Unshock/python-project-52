from django import template

from task_manager.statuses.models import Status
from task_manager.user.models import User


register = template.Library()

# #не исп
# @register.simple_tag()
# def get_users():
#     return User.objects.all()


# @register.simple_tag()
# def get_statuses():
#     return Status.objects.all()
