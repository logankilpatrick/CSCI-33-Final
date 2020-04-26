
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("<int:post_id>", views.editpost, name="editpost"),
    path("profile/<int:author_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<int:author_id>", views.follow, name="follow"),
    path("unfollow/<int:author_id>", views.unfollow, name="unfollow")
]
