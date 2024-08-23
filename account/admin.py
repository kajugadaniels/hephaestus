from django.contrib import admin
from account.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'email', 'phone_number', 'role', 'added_by', 'is_active', 'is_staff')
    search_fields = ('name', 'email', 'phone_number')
    prepopulated_fields = {'slug': ('name',)}