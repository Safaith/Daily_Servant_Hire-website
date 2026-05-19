from rest_framework import serializers
from .models import Booking
from servants.serializers import ServantListSerializer
from accounts.serializers import UserProfileSerializer

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['servant', 'service_date', 'service_address', 'special_instructions']

    def validate(self, data):
        servant = data['servant']
        service_date = data['service_date']
        hirer = self.context['request'].user
        if not servant.is_approved:
            raise serializers.ValidationError("This servant is not approved yet.")
        if servant.availability_status != 'available':
            raise serializers.ValidationError("This servant is not available.")
        if Booking.objects.filter(servant=servant, service_date=service_date,
                                   status__in=['pending', 'confirmed', 'in_progress']).exists():
            raise serializers.ValidationError("Servant is already booked on this date.")
        if Booking.objects.filter(hirer=hirer, servant=servant, service_date=service_date).exists():
            raise serializers.ValidationError("You already have a booking with this servant on this date.")
        return data

    def create(self, validated_data):
        servant = validated_data['servant']
        validated_data['hirer'] = self.context['request'].user
        validated_data['total_amount'] = servant.daily_rate
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    servant = ServantListSerializer(read_only=True)
    hirer = UserProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
