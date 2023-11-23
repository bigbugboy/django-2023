from django.urls import path

from . import views

urlpatterns = [
    path('todo', views.todolist),
    path('todo_create', views.todo_create),
    path('todo_status/<int:pk>', views.todo_status),
    path('todo_delete/<int:pk>', views.todo_delete),
]
