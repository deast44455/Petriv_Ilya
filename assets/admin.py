from django.contrib import admin
from .models import Category, Asset, Location, Department, Supplier, AssetOperation


class AssetOperationInline(admin.TabularInline):
    model = AssetOperation
    extra = 0
    readonly_fields = ['op_type', 'from_location', 'to_location', 'from_employee', 'to_employee', 'performed_by', 'performed_at', 'note']
    can_delete = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'prefix', 'description']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name', 'address']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn', 'phone', 'email']
    search_fields = ['name', 'inn']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['inventory_number', 'name', 'category', 'status', 'current_location', 'current_assignee', 'cost']
    list_filter = ['status', 'category', 'current_location']
    search_fields = ['name', 'inventory_number', 'serial_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AssetOperationInline]


@admin.register(AssetOperation)
class AssetOperationAdmin(admin.ModelAdmin):
    list_display = ['asset', 'op_type', 'performed_by', 'performed_at']
    list_filter = ['op_type', 'performed_at']
    search_fields = ['asset__name', 'asset__inventory_number']
    readonly_fields = ['performed_at']
