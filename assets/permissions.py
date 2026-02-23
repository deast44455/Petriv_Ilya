from rest_framework.permissions import BasePermission


class IsAdminOrStorekeeper(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.employee_profile.role in ('admin', 'storekeeper')
        except Exception:
            return False


class IsManagerOrAbove(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.employee_profile.role in ('admin', 'storekeeper', 'manager')
        except Exception:
            return False
