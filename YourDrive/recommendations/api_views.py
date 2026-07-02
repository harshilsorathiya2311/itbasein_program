from rest_framework import viewsets, permissions
from .models import RecommendationLog
from .serializers import RecommendationLogSerializer


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationLogSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return RecommendationLog.objects.all()
        return RecommendationLog.objects.filter(user=user)
