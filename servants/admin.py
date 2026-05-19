from django.contrib import admin
from .models import ServantProfile, ServiceCategory, Review

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_bn', 'icon']

@admin.register(ServantProfile)
class ServantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_rate', 'experience_years', 'rating', 'availability_status', 'is_approved']
    list_filter = ['is_approved', 'availability_status']
    list_editable = ['is_approved']
    actions = ['approve_servants']

    def approve_servants(self, request, queryset):
        queryset.update(is_approved=True)
    approve_servants.short_description = "Approve selected servants"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['servant', 'hirer', 'rating', 'created_at']
