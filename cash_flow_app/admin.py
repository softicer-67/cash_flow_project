from django.contrib import admin
from .models import Status, OperationType, Category, Subcategory, CashFlow


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'operation_type']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'status', 'operation_type', 'category', 'subcategory', 'amount']
    list_filter = ['created_date', 'status', 'operation_type']
