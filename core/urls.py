from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("register", UserView.register),
    path("login", UserView.login),
]