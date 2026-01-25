from rest_framework import serializers
from .models import DashboardMetric

class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
