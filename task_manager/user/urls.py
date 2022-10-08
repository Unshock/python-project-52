from django.urls import path
from task_manager.user import views


urlpatterns = [
    path("", views.Users.as_view(), name="users"),
    path("<int:user_id>/delete/", views.DeleteUser.as_view(), name="delete_user"),
    path("<int:user_id>/update/", views.UpdateUser.as_view(), name="update_user"),
    path("create/", views.CreateUser3.as_view(), name="create_user"),

]