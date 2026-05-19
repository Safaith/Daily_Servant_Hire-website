import uuid, random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Payment
from bookings.models import Booking

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    booking_id = request.data.get('booking_id')
    method = request.data.get('method')
    phone = request.data.get('phone_number', '')
    booking = get_object_or_404(Booking, id=booking_id, hirer=request.user)
    if hasattr(booking, 'payment') and booking.payment.status == 'completed':
        return Response({'error': 'Already paid.'}, status=400)
    payment, _ = Payment.objects.get_or_create(
        booking=booking,
        defaults={'amount': booking.total_amount, 'method': method, 'phone_number': phone}
    )
    payment.method = method
    payment.phone_number = phone
    payment.status = 'processing'
    payment.save()
    # Mock OTP generation
    otp = str(random.randint(100000, 999999))
    request.session[f'otp_{payment.id}'] = otp
    return Response({'payment_id': payment.id, 'otp_hint': f'Mock OTP: {otp}', 'amount': str(payment.amount)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    payment_id = request.data.get('payment_id')
    otp = request.data.get('otp')
    payment = get_object_or_404(Payment, id=payment_id, booking__hirer=request.user)
    session_otp = request.session.get(f'otp_{payment.id}')
    if str(otp) != str(session_otp):
        return Response({'error': 'Invalid OTP.'}, status=400)
    payment.status = 'completed'
    payment.transaction_id = f'DS-{uuid.uuid4().hex[:10].upper()}'
    payment.paid_at = timezone.now()
    payment.save()
    del request.session[f'otp_{payment.id}']
    return Response({'message': 'Payment successful!', 'transaction_id': payment.transaction_id})

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, hirer=request.user)
    existing_payment = getattr(booking, 'payment', None)
    return render(request, 'payments/payment.html', {'booking': booking, 'payment': existing_payment})

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, hirer=request.user)
    payment = getattr(booking, 'payment', None)
    return render(request, 'payments/success.html', {'booking': booking, 'payment': payment})
