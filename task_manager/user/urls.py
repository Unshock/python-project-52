from django.urls import path
from task_manager.user import views


urlpatterns = [
    path("", views.Users.as_view(), name="users"),
    path("<int:pk>/delete/", views.DeleteUser.as_view(), name="delete_user"),
    path("<int:pk>/update/", views.UpdateUser.as_view(), name="update_user"),
    path("<int:pk>/password/", views.ChangePassword.as_view(),
         name="password_change"),
    path("create/", views.CreateUser.as_view(), name="create_user"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout")
]