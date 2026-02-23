from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    prefix = models.CharField(max_length=10, blank=True, verbose_name='Префикс инв. номера')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=200, blank=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    inn = models.CharField(max_length=12, blank=True, verbose_name='ИНН')
    contact = models.CharField(max_length=200, blank=True, verbose_name='Контакт')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_IN_USE = 'in_use'
    STATUS_IN_STOCK = 'in_stock'
    STATUS_ASSIGNED = 'assigned'
    STATUS_IN_REPAIR = 'in_repair'
    STATUS_WRITTEN_OFF = 'written_off'

    STATUS_CHOICES = [
        (STATUS_IN_USE, 'В эксплуатации'),
        (STATUS_IN_STOCK, 'На складе'),
        (STATUS_ASSIGNED, 'Выдан'),
        (STATUS_IN_REPAIR, 'В ремонте'),
        (STATUS_WRITTEN_OFF, 'Списан'),
    ]

    name = models.CharField(max_length=200, verbose_name='Наименование')
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name='Инвентарный номер')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='Серийный номер')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='Дата приобретения')
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Стоимость')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_STOCK, verbose_name='Статус')
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Текущая локация')
    current_assignee = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets', verbose_name='Ответственный')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return f"{self.inventory_number} — {self.name}"

    @classmethod
    def generate_inventory_number(cls, category):
        prefix = category.prefix or 'A'
        year = datetime.date.today().year
        count = cls.objects.filter(category=category).count() + 1
        return f"{prefix}-{year}-{count:04d}"


class AssetOperation(models.Model):
    OP_RECEIPT = 'receipt'
    OP_TRANSFER = 'transfer'
    OP_ASSIGN = 'assign'
    OP_RETURN = 'return'
    OP_WRITEOFF = 'writeoff'
    OP_REPAIR_IN = 'repair_in'
    OP_REPAIR_OUT = 'repair_out'
    OP_INVENTORY = 'inventory_check'

    OP_CHOICES = [
        (OP_RECEIPT, 'Поступление'),
        (OP_TRANSFER, 'Перемещение'),
        (OP_ASSIGN, 'Выдача'),
        (OP_RETURN, 'Возврат'),
        (OP_WRITEOFF, 'Списание'),
        (OP_REPAIR_IN, 'Отправка в ремонт'),
        (OP_REPAIR_OUT, 'Возврат из ремонта'),
        (OP_INVENTORY, 'Инвентаризация'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='operations', verbose_name='Актив')
    op_type = models.CharField(max_length=20, choices=OP_CHOICES, verbose_name='Тип операции')
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations_from', verbose_name='Откуда')
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations_to', verbose_name='Куда')
    from_employee = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='operations_from', verbose_name='От сотрудника')
    to_employee = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='operations_to', verbose_name='Сотруднику')
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Выполнил')
    performed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата операции')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['-performed_at']

    def __str__(self):
        return f"{self.get_op_type_display()} — {self.asset} ({self.performed_at:%d.%m.%Y})"

    def clean(self):
        if not self.asset_id:
            return
        if self.op_type == self.OP_ASSIGN and self.asset.status == Asset.STATUS_WRITTEN_OFF:
            raise ValidationError('Нельзя назначить списанный актив.')
        if self.op_type == self.OP_RETURN and self.asset.status != Asset.STATUS_ASSIGNED:
            raise ValidationError('Нельзя вернуть актив, который не назначен.')
        if self.op_type == self.OP_WRITEOFF and self.asset.status == Asset.STATUS_WRITTEN_OFF:
            raise ValidationError('Актив уже списан.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        asset = self.asset
        if self.op_type == self.OP_RECEIPT:
            asset.status = Asset.STATUS_IN_STOCK
            if self.to_location:
                asset.current_location = self.to_location
        elif self.op_type == self.OP_ASSIGN:
            asset.status = Asset.STATUS_ASSIGNED
            asset.current_assignee = self.to_employee
            if self.to_location:
                asset.current_location = self.to_location
        elif self.op_type == self.OP_RETURN:
            asset.status = Asset.STATUS_IN_STOCK
            asset.current_assignee = None
            if self.to_location:
                asset.current_location = self.to_location
        elif self.op_type == self.OP_WRITEOFF:
            asset.status = Asset.STATUS_WRITTEN_OFF
            asset.current_assignee = None
        elif self.op_type == self.OP_REPAIR_IN:
            asset.status = Asset.STATUS_IN_REPAIR
        elif self.op_type == self.OP_REPAIR_OUT:
            asset.status = Asset.STATUS_IN_STOCK
            if self.to_location:
                asset.current_location = self.to_location
        elif self.op_type == self.OP_TRANSFER:
            asset.status = Asset.STATUS_IN_USE
            if self.to_location:
                asset.current_location = self.to_location
            if self.to_employee:
                asset.current_assignee = self.to_employee
        asset.save()
