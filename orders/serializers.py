from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model
    Converts Order objects to/from JSON for API responses
    """
    
    # Read-only fields
    order_number = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    is_delivered = serializers.BooleanField(read_only=True)
    has_driver = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'customer_email',
            'phone_number',
            'delivery_address',
            'delivery_city',
            'delivery_postal_code',
            'order_description',
            'order_status',
            'assigned_driver',
            'driver_notes',
            'pickup_time',
            'delivery_time',
            'current_latitude',
            'current_longitude',
            'delivery_photo_url',
            'created_at',
            'updated_at',
            'created_by',
            'is_delivered',
            'has_driver',
        ]
        
    def validate_phone_number(self, value):
        """
        Validate phone number format
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, +, -, and spaces")
        return value
    
    def validate_order_status(self, value):
        """
        Validate order status transitions
        """
        valid_statuses = ['PENDING', 'ASSIGNED', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating orders
    Only required fields
    """
    
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'phone_number',
            'delivery_address',
            'delivery_city',
            'order_description',
            'created_by',
        ]


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for drivers updating order status
    Used by Flutter app
    """
    
    class Meta:
        model = Order
        fields = [
            'order_status',
            'driver_notes',
            'current_latitude',
            'current_longitude',
            'delivery_photo_url',
            'pickup_time',
            'delivery_time',
        ]
        
    def validate(self, data):
        """
        Ensure delivered orders have delivery time
        """
        if data.get('order_status') == 'DELIVERED' and not data.get('delivery_time'):
            raise serializers.ValidationError(
                "Delivery time is required when marking order as delivered"
            )
        return data


class OrderListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing many orders
    Only essential fields for performance
    """
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'delivery_city',
            'order_status',
            'assigned_driver',
            'created_at',
        ]