from django.contrib import admin
from django.urls import path , include
from .views import login_teacher, logout, send_otp


urlpatterns = [
    path("login_teacher/", login_teacher, name="login_teacher"),
    path("logout/", logout, name="logout"),
    path("send_otp/", send_otp, name="send_otp"),


]