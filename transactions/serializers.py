from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'transaction_id' 'created_at', 'updated_at']
    
    def create(self, validated_data):
        import uuid
        validated_data['transaction_id'] = str(uuid.uuid4()) # Auto-generate ID
        return super().create(validated_data)
