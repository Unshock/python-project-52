from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager.user"
    verbose_name = "Пользователи сайта"