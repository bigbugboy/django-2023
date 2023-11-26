from django.urls import path

from . import views

urlpatterns = [
    path('', views.todolist, name='todolist'),
    path('add', views.add_todo),
    path('status/<int:pk>', views.change_status),
    path('delete/<int:pk>', views.delete_todo),
]
