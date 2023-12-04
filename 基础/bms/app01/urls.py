from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('activate_account', views.activate_account),
    path('home', views.home),
    path('login', views.login),
    path('vip', views.vip),
]
