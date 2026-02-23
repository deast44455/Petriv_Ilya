from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'position', 'is_responsible']
    list_filter = ['role', 'department', 'is_responsible']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
