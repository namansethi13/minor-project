from django.contrib import admin
from django.urls import path , include
from django.views.generic import TemplateView
from django_api_admin.sites import site
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)

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
    path('student_data/',student_data,name='student_data'),
    path('delete_student_data/',delete_student_data,name='delete_student_data'),
    path('format11/', format11,name ='format11'),
    path('format4/', format4,name ='format4'),
    path("check-student_data/", check_student_data,name ='check_student_data'),
    path("check_elective/", check_elective,name ='check_elective'),
    path('format5/', format5,name ='format5'),
    path('alladdedsubjects/', include(router.urls)),
    path('format13/', format13,name ='format13'),
    
    
    
   
] 