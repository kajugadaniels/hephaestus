from home.models import *
from django.contrib import admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'dob', 'gender', 'nationality', 
        'cell', 'village', 'sector', 'district', 
        'emergency_contact_name', 'emergency_contact_relation', 
        'emergency_contact_phone', 'created_at', 'updated_at'
    )
    search_fields = (
        'name', 'slug', 'cell', 'village', 
        'sector', 'district', 'emergency_contact_name', 
        'emergency_contact_relation', 'emergency_contact_phone'
    )
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('gender', 'nationality', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        # Optionally customize save behavior, e.g., setting additional fields
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing student
            return self.readonly_fields + ('slug',)
        return self.readonly_fields

    def age(self, obj):
        return obj.age
    age.admin_order_field = 'dob'
    age.short_description = 'Age'