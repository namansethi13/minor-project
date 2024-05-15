from django.contrib import admin
from django.urls import path , include
from .views import *
urlpatterns = [
    path("result/", result,name ='result'),
    path("result/<int:id>", result_id,name ='result_id'),
    path("getcourse/<int:id>", getcourse,name ='getcourse'),
    
]