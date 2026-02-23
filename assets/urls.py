from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('locations', views.LocationViewSet)
router.register('departments', views.DepartmentViewSet)
router.register('suppliers', views.SupplierViewSet)
router.register('assets', views.AssetViewSet)
router.register('operations', views.AssetOperationViewSet)

urlpatterns = router.urls
