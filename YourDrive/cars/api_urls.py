from rest_framework.routers import DefaultRouter
from .api_views import CarViewSet, BrandViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'brands', BrandViewSet)

urlpatterns = router.urls
