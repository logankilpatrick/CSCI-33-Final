
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newschool", views.newschool, name="newschool"),
    path("newprogram", views.newprogram, name="newprogram"),
    path("<int:post_id>", views.editpost, name="editpost"),
    path("profile/<int:schoolID>", views.profile, name="profile"),
    path("profile/<str:schoolName>/<str:programName>", views.program, name="program"),
    path("following", views.following, name="following"),
    path("follow/<str:schoolName>", views.follow, name="follow"),
    path("unfollow/<str:schoolName>", views.unfollow, name="unfollow"),
    path("userprofile/<int:studentID>", views.userprofile, name="userprofile"),
    
    # API Routes
    path("chathome", views.chatindex, name="chatindex"),
    path("chat", views.compose, name="compose"),
    path("chat/<int:email_id>", views.chat, name="chat"),
    path("chat/<str:mailbox>", views.chatbox, name="chatbox"),

    
]
