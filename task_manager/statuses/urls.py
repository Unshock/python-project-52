from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path("", views.Statuses.as_view(), name="statuses"),
    path("create/", views.CreateStatus.as_view(), name="create_status"),
    path("<int:status_id>/update/", views.UpdateStatus.as_view(), name="update_status"),
    path("<int:status_id>/delete/", views.DeleteStatus.as_view(), name="delete_status"),

]