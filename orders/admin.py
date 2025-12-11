from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Order model
    Provides a powerful interface for managing orders
    """
    
    # List view configuration
    list_display = [
        'order_number',
        'customer_name',
        'phone_number',
        'delivery_city',
        'order_status',
        'assigned_driver',
        'created_at',
        'is_delivered',
    ]
    
    list_filter = [
        'order_status',
        'delivery_city',
        'created_at',
        'updated_at',
    ]
    
    search_fields = [
        'order_number',
        'customer_name',
        'phone_number',
        'delivery_address',
        'assigned_driver',
    ]
    
    # Detail view configuration
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'order_status', 'order_description')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'phone_number')
        }),
        ('Delivery Details', {
            'fields': (
                'delivery_address', 
                'delivery_city', 
                'delivery_postal_code'
            )
        }),
        ('Driver Assignment', {
            'fields': ('assigned_driver', 'driver_notes')
        }),
        ('Tracking', {
            'fields': (
                'pickup_time',
                'delivery_time',
                'current_latitude',
                'current_longitude',
                'delivery_photo_url',
            )
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    # Ordering
    ordering = ['-created_at']
    
    # Number of items per page
    list_per_page = 25
    
    # Enable date hierarchy navigation
    date_hierarchy = 'created_at'
    
    # Actions
    actions = ['mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_delivered(self, request, queryset):
        """
        Custom admin action to mark orders as delivered
        """
        updated = queryset.update(order_status='DELIVERED')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as Delivered'
    
    def mark_as_cancelled(self, request, queryset):
        """
        Custom admin action to mark orders as cancelled
        """
        updated = queryset.update(order_status='CANCELLED')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark selected orders as Cancelled'