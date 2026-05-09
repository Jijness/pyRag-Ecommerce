from rest_framework import serializers
from .models import Payment, TransactionLog, Refund


class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['id', 'event_type', 'gateway_transaction_id', 'response_message', 'logged_at']


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'order_id', 'amount', 'reason', 'status', 'requested_at', 'resolved_at']


class PaymentSerializer(serializers.ModelSerializer):
    transaction_logs = TransactionLogSerializer(many=True, read_only=True)
    refund = RefundSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'customer_id', 'amount', 'currency',
            'method_type', 'status', 'gateway_ref', 'created_at', 'paid_at',
            'transaction_logs', 'refund',
        ]
