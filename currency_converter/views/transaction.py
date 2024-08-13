from rest_framework import permissions, viewsets

from currency_converter.models import Transaction
from currency_converter.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or edited.
    """

    queryset = Transaction.objects.all().order_by("timestamp")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
