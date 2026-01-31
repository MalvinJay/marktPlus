from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['transaction_id', 'transaction_id', 'payment_method']
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Get all transactions for the authenticated user 
    @action(detail=False, methods=['get'])
    def Index(self, request):
        transactions = self.get_queryset().all()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    # Create a new transaction
    @action(detail=False, methods=['post'])
    def Index(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaction successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get transactions by status
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_filter = request.query_params.get('status')
        if status_filter:
            transactions = self.get_queryset().filter(status=status_filter)
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)
        return Response({'error': 'Status parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    # Update transaction 
    @action(detail=True, methods=['put'])
    def Index(self, request, pk=None):
        transaction = request.user.transactions.get(pk=pk)
        serializer = self.get_serializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Update transaction status
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        transaction = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Transaction.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        transaction.status = new_status
        transaction.save()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)    

