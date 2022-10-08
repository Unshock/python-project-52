from django import template
from task_manager.user.models import User

register = template.Library()


@register.simple_tag()
def get_users():
    return User.objects.all()
