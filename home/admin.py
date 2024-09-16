from django.contrib import admin
from home.models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'dob', 'gender', 'nationality', 
        'cell', 'village', 'sector', 'district', 'current_status',
        'emergency_contact_name', 'emergency_contact_relation', 
        'emergency_contact_phone', 'created_at', 'updated_at'
    )
    search_fields = (
        'name', 'slug', 'cell', 'village', 'current_status',
        'sector', 'district', 'emergency_contact_name', 
        'emergency_contact_relation', 'emergency_contact_phone'
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('gender', 'nationality', 'current_status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

    def age(self, obj):
        return obj.age
    age.admin_order_field = 'dob'
    age.short_description = 'Age'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'position', 'department', 'employment_status', 'date_joined', 'delete_status')
    search_fields = ('name', 'employee_id', 'position', 'department', 'subjects_taught')  # Modified
    list_filter = ('gender', 'employment_status', 'delete_status', 'date_joined')
    readonly_fields = ('created_at', 'updated_at')

    def name(self, obj):
        return obj.name

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'delete_status')
    search_fields = ('name',)
    list_filter = ('delete_status',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'start_date', 'end_date', 'delete_status')
    search_fields = ('name', 'academic_year__name')
    list_filter = ('academic_year', 'delete_status')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'section', 'head_teacher', 'capacity', 'academic_year', 'delete_status')
    search_fields = ('name', 'grade', 'section', 'head_teacher__user__name')
    list_filter = ('grade', 'academic_year', 'delete_status')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'delete_status')
    search_fields = ('name', 'code')
    list_filter = ('delete_status',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'subject', 'teacher', 'starting_hour', 'ending_hour', 'delete_status')
    search_fields = ('class_group__name', 'subject__name', 'teacher__user__name')
    list_filter = ('delete_status',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_subject', 'date', 'status')
    search_fields = ('student__name', 'class_subject__subject__name')
    list_filter = ('status', 'date')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)
    list_filter = ('date',)
    readonly_fields = ('created_at', 'updated_at')