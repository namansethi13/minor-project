from django.contrib import admin
from django.urls import path , include
from .views import login_teacher, logout, send_otp,test_login,resetadminpassword,testversion
from django_api_admin.sites import site


urlpatterns = [
    path("login_teacher/", login_teacher, name="login_teacher"),
    path("logout/", logout, name="logout"),
    path("send_otp/", send_otp, name="send_otp"),
    path("test_login/", test_login, name="test_login"),
    path('api_admin/', site.urls),
    path('resetadminpassword/', resetadminpassword, name='resetadminpassword'),
    path('testversion/', testversion, name='testversion')



]