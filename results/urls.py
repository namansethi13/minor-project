from django.contrib import admin
from django.urls import path , include
from django.views.generic import TemplateView
from django_api_admin.sites import site

from .views import *
urlpatterns = [
    path("normalize/", normalize,name ='normalize'),
    path("normalize_page/", TemplateView.as_view(template_name='normalize.html'),name ='normalize_page'),
    path("convert/", convert,name ='convert'),
    path("check-result/", check_result,name ='check_result'),
    path('download-result/<int:id>', download_result,name ='download_result'),
    path('update-result/', update_result,name ='update_result'),
    path('format1/', format1,name ='format1'),
    path('format2/', format2,name ='format2'),
    path('format6/', format6,name ='format6'),
    path('format7/', format7,name ='format6'),
    path('get_all_subjects/',getallsubjects,name='getallsubjects'),
    path('get_all_courses/',getallcourses,name='getallcourses'),
    path('format11/', format11,name ='format11'),
    
   
] 