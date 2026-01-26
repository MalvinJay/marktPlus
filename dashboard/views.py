from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DashboardMetric
from .serializers import DashboardMetricSerializer
from transactions.models import Transaction
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.
class DashboardViewSet(viewsets.ViewSet):
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DashboardMetric.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        last_30_days = timezone.now() - timedelta(days=30)
        recent_transactions = transactions.filter(created_at__gte=last_30_days)

        summary = {
            'total_revenue': float(transactions.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0), # (total=Sum('amount'))['total'] or 0)
            'total_transactions': transactions.count(),
            'completed_transactions': transactions.filter(status='completed').count(),
            'pending_transactions': transactions.filter(status='pending').count(),
            'failed_transactions': transactions.filter(status='failed').count(),
            'last_30_days_revenue': float(recent_transactions.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0), # (total=Sum('amount'))['total'] or 0)
        }
        return Response(summary, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        last_7_days = timezone.now() - timedelta(days=7)
        recent_transactions = Transaction.objects.filter(user=user, created_at__gte=last_7_days)
        
        daily_stats = []
        for i in range(7):
            day = timezone.now() - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_revenue = float(recent_transactions.filter(
                created_at__gte=day_start,
                created_at__lt=day_end,
                status='completed'
            ).aggregate(Sum('amount'))['amount__sum'] or 0)
            
            daily_stats.append({
                'date': day.date(),
                'revenue': day_revenue,
                'transactions': recent_transactions.filter(created_at__gte=day_start, created_at__lt=day_end).count()
            })
        
        return Response({'daily_stats': daily_stats})

