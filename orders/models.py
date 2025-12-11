from django.db import models
from django.core.validators import RegexValidator

class Order(models.Model):
    """
    Order model for logistics management system
    Used by both Flutter app (drivers) and Power Apps (managers)
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned to Driver'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Customer Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    
    # Delivery Information
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100, default='Manila')
    delivery_postal_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Order Details
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    order_description = models.TextField(blank=True, null=True)
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    # Driver Assignment
    assigned_driver = models.CharField(max_length=200, blank=True, null=True)
    driver_notes = models.TextField(blank=True, null=True)
    
    # Delivery Tracking
    pickup_time = models.DateTimeField(blank=True, null=True)
    delivery_time = models.DateTimeField(blank=True, null=True)
    
    # Location Data (for Flutter app GPS tracking)
    current_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True
    )
    current_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True
    )
    
    # Photo Evidence (URL from Flutter app)
    delivery_photo_url = models.URLField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=200, default='System')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate order number if not exists
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_delivered(self):
        return self.order_status == 'DELIVERED'
    
    @property
    def has_driver(self):
        return bool(self.assigned_driver)