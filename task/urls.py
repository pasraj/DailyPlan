from django.urls import path
from . views import task_view, login_view, logout_view, create_task

urlpatterns = [
    path('', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('task/', task_view, name="task"),
    path('task/create/', create_task, name="create-task"),
    path('task/update/<int:pk>/', create_task, name="update-taks"),
]
