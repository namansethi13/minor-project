from django.contrib import admin
from django.urls import path , include
from django.views.generic import TemplateView

from .views import *
urlpatterns = [
    path("normalize/", normalize,name ='normalize'),
    path("normalize_page/", TemplateView.as_view(template_name='normalize.html'),name ='normalize_page'),
    path("convert/", convert,name ='convert'),
    path("check-result/", check_result,name ='check_result'),
    

]