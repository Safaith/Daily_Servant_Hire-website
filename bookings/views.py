from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from servants.models import ServantProfile

class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_hirer():
            return Booking.objects.filter(hirer=user)
        elif user.is_servant():
            return Booking.objects.filter(servant=user.servant_profile)
        return Booking.objects.all()

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    user = request.user
    new_status = request.data.get('status')
    
    if user.is_servant() and hasattr(user, 'servant_profile') and booking.servant == user.servant_profile:
        if new_status in ['confirmed', 'rejected', 'in_progress', 'completed']:
            booking.status = new_status
            booking.save()
            return Response({'status': booking.status})
    elif user.is_hirer() and booking.hirer == user:
        if new_status == 'cancelled':
            booking.status = 'cancelled'
            booking.cancelled_reason = request.data.get('reason', '')
            booking.save()
            return Response({'status': booking.status})
    return Response({'error': 'Not authorized.'}, status=403)

# Template Views
@login_required
def book_servant(request, servant_id):
    servant = get_object_or_404(ServantProfile, pk=servant_id, is_approved=True)
    if not request.user.is_hirer():
        messages.error(request, 'Only hirers can book servants.')
        return redirect('servant_detail', pk=servant_id)
    if request.method == 'POST':
        from .forms import BookingForm
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hirer = request.user
            booking.servant = servant
            booking.total_amount = servant.daily_rate
            # Check conflicts
            if Booking.objects.filter(servant=servant, service_date=booking.service_date,
                                       status__in=['pending', 'confirmed', 'in_progress']).exists():
                messages.error(request, 'Servant is already booked on this date.')
            else:
                booking.save()
                messages.success(request, 'Booking submitted! Awaiting servant confirmation. 🎯')
                return redirect('hirer_dashboard')
    else:
        from .forms import BookingForm
        form = BookingForm()
    return render(request, 'bookings/book.html', {'servant': servant, 'form': form})

@login_required
def hirer_dashboard(request):
    if not request.user.is_hirer():
        return redirect('home')
    bookings = Booking.objects.filter(hirer=request.user).select_related('servant__user').order_by('-created_at')
    return render(request, 'bookings/hirer_dashboard.html', {'bookings': bookings})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, hirer=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    return redirect('hirer_dashboard')

@login_required
def servant_respond_booking(request, pk):
    profile = getattr(request.user, 'servant_profile', None)
    booking = get_object_or_404(Booking, pk=pk, servant=profile)
    action = request.POST.get('action')
    if action == 'confirm':
        booking.status = 'confirmed'
        messages.success(request, 'Booking confirmed! ✅')
    elif action == 'reject':
        booking.status = 'rejected'
        messages.info(request, 'Booking rejected.')
    elif action == 'complete':
        booking.status = 'completed'
        profile.total_jobs += 1
        profile.save()
        messages.success(request, 'Job marked as completed! 🎉')
    booking.save()
    return redirect('servant_dashboard')
