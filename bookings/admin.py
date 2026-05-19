from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'hirer', 'servant', 'service_date', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'service_date']
    search_fields = ['hirer__username', 'servant__user__username']
