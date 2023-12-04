from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list),
    path('list', views.book_list, name='book_list'),
    path('create', views.book_create, name='book_create'),
    path('edit/<int:book_id>', views.book_edit),
    path('delete/<int:book_id>', views.book_delete),
]
