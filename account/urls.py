from django.urls import path

from .views import login, logout, callback, home

urlpatterns = [
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("callback", callback, name="callback"),
    path("home/", home, name="home"),
]
