from rest_framework import serializers
from .models import Payment
import uuid

class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source='get_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['transaction_id', 'status', 'paid_at']

class PaymentInitiateSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=['bkash', 'nagad', 'rocket', 'card', 'cash'])
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)

class PaymentConfirmSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)  # Mock OTP verification
