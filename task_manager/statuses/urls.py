from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path("", views.Statuses.as_view(), name="statuses"),
    path("create/", views.stab, name="create_status"),
    path("<int:status_id>/update/", views.stab, name="update_status"),
    path("<int:status_id>/delete/", views.stab, name="delete_status"),

]