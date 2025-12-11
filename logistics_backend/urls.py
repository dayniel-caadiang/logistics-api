"""
Main URL Configuration for logistics_backend project
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# API Documentation with Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Logistics Management API",
        default_version='v1',
        description="""
        REST API for Logistics Management System
        
        This API serves both:
        - Flutter Mobile App (Drivers/Field Workers)
        - Power Apps (Office Managers)
        
        Features:
        - Complete CRUD operations for orders
        - Driver assignment and tracking
        - Real-time status updates
        - GPS location tracking
        - Search and filtering
        """,
        contact=openapi.Contact(email="support@logistics.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router for REST API endpoints
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Health check endpoint
    path('', lambda request: None),  # Add a simple health check view in production
]

"""
Available API Endpoints:

Base URL: http://localhost:8000/api/

CRUD Operations:
- GET    /api/orders/                  - List all orders
- POST   /api/orders/                  - Create new order
- GET    /api/orders/{id}/             - Get single order
- PUT    /api/orders/{id}/             - Update entire order
- PATCH  /api/orders/{id}/             - Partial update
- DELETE /api/orders/{id}/             - Delete order

Custom Actions:
- PATCH  /api/orders/{id}/update_status/  - Quick status update (for drivers)
- GET    /api/orders/by_driver/           - Filter by driver (?driver=John)
- GET    /api/orders/by_status/           - Filter by status (?status=PENDING)
- GET    /api/orders/search/              - Search orders (?q=search_term)

Filtering (on list endpoint):
- GET /api/orders/?status=PENDING
- GET /api/orders/?driver=John
- GET /api/orders/?city=Manila

Documentation:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
"""