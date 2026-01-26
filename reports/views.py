from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer
from transactions.models import Transaction
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['generated_at']
    ordering = ['-generated_at']

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def generate_revenue_report(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date required'}, status=status.HTTP_400_BAD_REQUEST)
        
        transactions = Transaction.objects.filter(
            user=request.user,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
        
        data = {
            'total_revenue': float(transactions.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0),
            'transaction_count': transactions.count(),
            'by_type': dict(transactions.values('type').annotate(count=Count('id')).values_list('type', 'count'))
        }
        
        report = Report.objects.create(
            user=request.user,
            title=f'Revenue Report {start_date} to {end_date}',
            report_type='revenue',
            data=data,
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
