from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    ROLES = [
        ('admin', 'Администратор'),
        ('storekeeper', 'Кладовщик'),
        ('manager', 'Руководитель'),
        ('employee', 'Сотрудник'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    role = models.CharField(max_length=20, choices=ROLES, default='employee')
    department = models.ForeignKey('assets.Department', on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    is_responsible = models.BooleanField(default=False, verbose_name='МОЛ')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
