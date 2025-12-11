from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Order
from .serializers import (
    OrderSerializer, 
    OrderCreateSerializer,
    OrderUpdateStatusSerializer,
    OrderListSerializer
)

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order CRUD operations
    
    Provides:
    - list: GET /api/orders/
    - create: POST /api/orders/
    - retrieve: GET /api/orders/{id}/
    - update: PUT /api/orders/{id}/
    - partial_update: PATCH /api/orders/{id}/
    - destroy: DELETE /api/orders/{id}/
    
    Custom actions:
    - update_status: PATCH /api/orders/{id}/update_status/
    - by_driver: GET /api/orders/by_driver/?driver=DriverName
    - by_status: GET /api/orders/by_status/?status=PENDING
    - search: GET /api/orders/search/?q=customer_name
    """
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderUpdateStatusSerializer
        return OrderSerializer
    
    def list(self, request):
        """
        List all orders with optional filtering
        
        Query params:
        - status: Filter by order_status
        - driver: Filter by assigned_driver
        - city: Filter by delivery_city
        """
        queryset = self.get_queryset()
        
        # Optional filters
        status_filter = request.query_params.get('status', None)
        driver_filter = request.query_params.get('driver', None)
        city_filter = request.query_params.get('city', None)
        
        if status_filter:
            queryset = queryset.filter(order_status=status_filter.upper())
        if driver_filter:
            queryset = queryset.filter(assigned_driver__icontains=driver_filter)
        if city_filter:
            queryset = queryset.filter(delivery_city__icontains=city_filter)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def create(self, request):
        """
        Create a new order
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            # Return full order details
            response_serializer = OrderSerializer(order)
            return Response(
                response_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Get a single order by ID
        """
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, pk=None):
        """
        Update an entire order (PUT)
        """
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def partial_update(self, request, pk=None):
        """
        Partially update an order (PATCH)
        """
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk=None):
        """
        Delete an order
        """
        try:
            order = self.get_queryset().get(pk=pk)
            order.delete()
            return Response(
                {'message': 'Order deleted successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Custom action for drivers to update order status
        PATCH /api/orders/{id}/update_status/
        
        Used by Flutter app for quick status updates
        """
        try:
            order = self.get_queryset().get(pk=pk)
            serializer = OrderUpdateStatusSerializer(
                order, 
                data=request.data, 
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                # Return full order details
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def by_driver(self, request):
        """
        Get orders assigned to a specific driver
        GET /api/orders/by_driver/?driver=John
        """
        driver_name = request.query_params.get('driver', None)
        if not driver_name:
            return Response(
                {'error': 'Driver parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = self.get_queryset().filter(assigned_driver__icontains=driver_name)
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'driver': driver_name,
            'count': orders.count(),
            'orders': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        Get orders by status
        GET /api/orders/by_status/?status=PENDING
        """
        order_status = request.query_params.get('status', None)
        if not order_status:
            return Response(
                {'error': 'Status parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = self.get_queryset().filter(order_status=order_status.upper())
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'status': order_status.upper(),
            'count': orders.count(),
            'orders': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search orders by customer name, order number, or address
        GET /api/orders/search/?q=search_term
        """
        query = request.query_params.get('q', None)
        if not query:
            return Response(
                {'error': 'Search query parameter (q) is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = self.get_queryset().filter(
            Q(customer_name__icontains=query) |
            Q(order_number__icontains=query) |
            Q(delivery_address__icontains=query) |
            Q(phone_number__icontains=query)
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({
            'query': query,
            'count': orders.count(),
            'results': serializer.data
        })