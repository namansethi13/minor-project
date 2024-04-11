from django.contrib import admin
from django_api_admin.sites import site as api_admin_site

# Register your models here.
from .models import *
# admin.site.register([Result,Subject,Course])
api_admin_site.register(Result)
api_admin_site.register(Subject)
api_admin_site.register(Course)
