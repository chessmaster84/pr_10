"""
URL configuration for site_pr10 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path


from grades import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    re_path(r'^students/$', views.students_list, name='students_list'),
    re_path(r'^students/(?P<student_code>[a-z_]+)/$', views.student_details, name='student_details'),
    re_path(r'^tests/$', views.tests_list, name='tests_list'),
    re_path(r'^tests/(?P<task_id>\d+)/$', views.test_details, name='test_details'),

]
