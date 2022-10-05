from django.urls import path
from task_manager.user import views


urlpatterns = [
    path("", views.Users.as_view()),
    path("<int:user_id>/delete/", views.DeleteUser.as_view()),
    path("sign_up/", views.CreateUser.as_view()),
    path("postuser/", views.CreateUser.post),
]