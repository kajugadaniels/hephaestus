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

    path('teachers/', getTeachers, name='getTeachers'),
    path('teacher/add/', addTeacher, name='addTeacher'),
    path('teacher/<str:employee_id>/', viewTeacher, name='viewTeacher'),
    path('teacher/<str:employee_id>/edit/', editTeacher, name='editTeacher'),
    path('teacher/<str:employee_id>/delete/', deleteTeacher, name='deleteTeacher'),

    path('academic-years/', getAcademicYears, name='getAcademicYears'),
    path('academic-year/add/', addAcademicYear, name='addAcademicYear'),
    path('academic-year/<int:id>/', viewAcademicYear, name='viewAcademicYear'),
    path('academic-year/<int:id>/edit/', editAcademicYear, name='editAcademicYear'),
    path('academic-year/<int:id>/delete/', deleteAcademicYear, name='deleteAcademicYear'),

    path('terms/', getTerms, name='getTerms'),
    path('term/add/', addTerm, name='addTerm'),
    path('term/<int:id>/', viewTerm, name='viewTerm'),
    path('term/<int:id>/edit/', editTerm, name='editTerm'),
    path('term/<int:id>/delete/', deleteTerm, name='deleteTerm'),

    path('classes/', getClasses, name='getClasses'),
    path('class/add/<str:academic_year_id>', addClass, name='addClass'),
    path('class/<int:id>/', viewClass, name='viewClass'),
    path('class/<int:id>/edit/', editClass, name='editClass'),
    path('class/<int:id>/delete/', deleteClass, name='deleteClass'),

    path('subjects/', getSubjects, name='getSubjects'),
    path('subject/add/', addSubject, name='addSubject'),
    path('subject/<int:id>/', viewSubject, name='viewSubject'),
    path('subject/<int:id>/edit/', editSubject, name='editSubject'),
    path('subject/<int:id>/delete/', deleteSubject, name='deleteSubject'),

    path('class/<int:class_id>/subjects/', getClassSubjects, name='getClassSubjects'),
    path('class/<int:class_id>/assign-subjects/', assignSubjects, name='assignSubjects'),
    path('class-subject/<int:id>/edit/', editClassSubject, name='editClassSubject'),
    path('class-subject/<int:id>/delete/', deleteClassSubject, name='deleteClassSubject'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)