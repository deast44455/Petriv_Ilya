from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Location, Department, Supplier, Asset, AssetOperation
from .serializers import (
    CategorySerializer, LocationSerializer, DepartmentSerializer,
    SupplierSerializer, AssetSerializer, AssetOperationSerializer,
)
from .permissions import IsAdminOrStorekeeper, IsManagerOrAbove


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'address']
    ordering_fields = ['name']


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'inn']
    ordering_fields = ['name']


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.select_related('category', 'supplier', 'current_location', 'current_assignee').all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category', 'current_location', 'current_assignee']
    search_fields = ['name', 'inventory_number', 'serial_number']
    ordering_fields = ['name', 'inventory_number', 'cost', 'created_at']


class AssetOperationViewSet(viewsets.ModelViewSet):
    queryset = AssetOperation.objects.select_related('asset', 'performed_by', 'from_location', 'to_location', 'from_employee', 'to_employee').all()
    serializer_class = AssetOperationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStorekeeper]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['asset', 'op_type', 'performed_by']
    search_fields = ['asset__name', 'asset__inventory_number', 'note']
    ordering_fields = ['performed_at']

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)
