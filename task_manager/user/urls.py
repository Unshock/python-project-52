from django.urls import path
from task_manager.user import views


urlpatterns = [
    path("create/", views.CreateUser.as_view()),
    path("postuser/", views.CreateUser.post),
]