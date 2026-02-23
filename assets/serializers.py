from rest_framework import serializers
from .models import Category, Location, Department, Supplier, Asset, AssetOperation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AssetOperationSerializer(serializers.ModelSerializer):
    op_type_display = serializers.CharField(source='get_op_type_display', read_only=True)
    performed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AssetOperation
        fields = '__all__'
        read_only_fields = ['performed_by', 'performed_at']

    def validate(self, attrs):
        asset = attrs.get('asset')
        op_type = attrs.get('op_type')
        if asset and op_type:
            if op_type == AssetOperation.OP_ASSIGN and asset.status == Asset.STATUS_WRITTEN_OFF:
                raise serializers.ValidationError('Нельзя назначить списанный актив.')
            if op_type == AssetOperation.OP_RETURN and asset.status != Asset.STATUS_ASSIGNED:
                raise serializers.ValidationError('Нельзя вернуть актив, который не назначен.')
            if op_type == AssetOperation.OP_WRITEOFF and asset.status == Asset.STATUS_WRITTEN_OFF:
                raise serializers.ValidationError('Актив уже списан.')
        return attrs
