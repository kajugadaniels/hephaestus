from django.urls import path
from django.conf import settings
from home.views import *
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('dashboard', dashboard, name="dashboard"),

    path('users/', getUsers, name='getUsers'),
    path('user/add', addUser, name='addUser'),

    path('upload_image/', upload_image, name='upload_image'),

    path('students/', getStudents, name='getStudents'),
    path('student/add', addStudent, name='addStudent'),
    path('student/<slug:slug>', viewStudent, name='viewStudent'),
    path('student/<slug:slug>/edit', editStudent, name='editStudent'),
    path('student/<slug:slug>/delete', deleteStudent, name='deleteStudent'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)