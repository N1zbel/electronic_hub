from rest_framework import viewsets
from .models import Supplier
from .permissions import IsActiveEmployee
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        country_filter = self.request.query_params.get('country', None)
        queryset = super().get_queryset()
        if country_filter:
            queryset = queryset.filter(country=country_filter)
        return queryset

    def perform_update(self, serializer):
        serializer.save(debt_to_supplier=self.get_object().debt_to_supplier)
