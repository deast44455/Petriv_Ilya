from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from assets.models import Category, Location, Asset, AssetOperation
from accounts.models import Employee


class AssetOperationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.category = Category.objects.create(name='Компьютеры', prefix='PC')
        self.location = Location.objects.create(name='Склад')
        self.employee = Employee.objects.create(user=self.user, role='storekeeper')
        self.asset = Asset.objects.create(
            name='Ноутбук Dell',
            inventory_number='PC-2024-0001',
            category=self.category,
            status=Asset.STATUS_IN_STOCK,
        )

    def test_create_asset(self):
        asset = Asset.objects.create(
            name='Принтер HP',
            inventory_number='PC-2024-0002',
            category=self.category,
        )
        self.assertEqual(asset.status, Asset.STATUS_IN_STOCK)
        self.assertIsNotNone(asset.pk)

    def test_assign_operation(self):
        op = AssetOperation(
            asset=self.asset,
            op_type=AssetOperation.OP_ASSIGN,
            to_employee=self.employee,
            to_location=self.location,
            performed_by=self.user,
        )
        op.save()
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.status, Asset.STATUS_ASSIGNED)
        self.assertEqual(self.asset.current_assignee, self.employee)

    def test_return_operation(self):
        # First assign
        AssetOperation.objects.create(
            asset=self.asset,
            op_type=AssetOperation.OP_ASSIGN,
            to_employee=self.employee,
            to_location=self.location,
            performed_by=self.user,
        )
        self.asset.refresh_from_db()
        # Then return
        AssetOperation.objects.create(
            asset=self.asset,
            op_type=AssetOperation.OP_RETURN,
            from_employee=self.employee,
            to_location=self.location,
            performed_by=self.user,
        )
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.status, Asset.STATUS_IN_STOCK)
        self.assertIsNone(self.asset.current_assignee)

    def test_writeoff_operation(self):
        AssetOperation.objects.create(
            asset=self.asset,
            op_type=AssetOperation.OP_WRITEOFF,
            performed_by=self.user,
        )
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.status, Asset.STATUS_WRITTEN_OFF)

    def test_cannot_assign_written_off_asset(self):
        self.asset.status = Asset.STATUS_WRITTEN_OFF
        self.asset.save()
        op = AssetOperation(
            asset=self.asset,
            op_type=AssetOperation.OP_ASSIGN,
            to_employee=self.employee,
            performed_by=self.user,
        )
        with self.assertRaises(ValidationError):
            op.clean()

    def test_cannot_return_not_assigned_asset(self):
        # Asset is in_stock, not assigned
        self.assertEqual(self.asset.status, Asset.STATUS_IN_STOCK)
        op = AssetOperation(
            asset=self.asset,
            op_type=AssetOperation.OP_RETURN,
            from_employee=self.employee,
            performed_by=self.user,
        )
        with self.assertRaises(ValidationError):
            op.clean()
