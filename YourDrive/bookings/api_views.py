from rest_framework import viewsets, permissions
from .models import TestDriveBooking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TestDriveBooking.objects.all()
        return TestDriveBooking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
