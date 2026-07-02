from rest_framework.routers import DefaultRouter
from .api_views import RecommendationViewSet

router = DefaultRouter()
router.register(r'logs', RecommendationViewSet, basename='recommendationlog')

urlpatterns = router.urls
