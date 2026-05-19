from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ServantProfile, ServiceCategory, Review
from .serializers import ServantProfileSerializer, ServantListSerializer, ServiceCategorySerializer, ReviewSerializer
from .forms import ServantProfileForm

# API Views
class ServantListAPIView(generics.ListAPIView):
    serializer_class = ServantListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'location', 'skills']
    ordering_fields = ['daily_rate', 'rating', 'experience_years']

    def get_queryset(self):
        qs = ServantProfile.objects.filter(is_approved=True).select_related('user').prefetch_related('categories')
        category = self.request.query_params.get('category')
        min_rate = self.request.query_params.get('min_rate')
        max_rate = self.request.query_params.get('max_rate')
        availability = self.request.query_params.get('availability')
        if category:
            qs = qs.filter(categories__id=category)
        if min_rate:
            qs = qs.filter(daily_rate__gte=min_rate)
        if max_rate:
            qs = qs.filter(daily_rate__lte=max_rate)
        if availability:
            qs = qs.filter(availability_status=availability)
        return qs

class ServantDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ServantProfileSerializer
    permission_classes = [AllowAny]
    queryset = ServantProfile.objects.filter(is_approved=True)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_review(request, servant_id):
    servant = get_object_or_404(ServantProfile, id=servant_id)
    if request.user == servant.user:
        return Response({'error': 'Cannot review yourself.'}, status=400)
    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review, created = Review.objects.update_or_create(
        servant=servant, hirer=request.user,
        defaults={'rating': serializer.validated_data['rating'], 'comment': serializer.validated_data['comment']}
    )
    # Recalculate average rating
    reviews = servant.reviews.all()
    servant.rating = sum(r.rating for r in reviews) / reviews.count()
    servant.total_reviews = reviews.count()
    servant.save()
    return Response(ReviewSerializer(review).data, status=201 if created else 200)

# Template Views
def servant_list_view(request):
    categories = ServiceCategory.objects.all()
    servants = ServantProfile.objects.filter(is_approved=True).select_related('user').prefetch_related('categories')
    
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    min_rate = request.GET.get('min_rate', '')
    max_rate = request.GET.get('max_rate', '')
    sort = request.GET.get('sort', '-rating')

    if query:
        servants = servants.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(skills__icontains=query) |
            Q(location__icontains=query)
        )
    if category_id:
        servants = servants.filter(categories__id=category_id)
    if min_rate:
        servants = servants.filter(daily_rate__gte=min_rate)
    if max_rate:
        servants = servants.filter(daily_rate__lte=max_rate)
    servants = servants.order_by(sort)

    return render(request, 'servants/list.html', {
        'servants': servants, 'categories': categories,
        'query': query, 'category_id': category_id,
    })

def servant_detail_view(request, pk):
    servant = get_object_or_404(ServantProfile, pk=pk, is_approved=True)
    reviews = servant.reviews.select_related('hirer').order_by('-created_at')
    can_review = False
    if request.user.is_authenticated and request.user.is_hirer():
        from bookings.models import Booking
        can_review = Booking.objects.filter(
            hirer=request.user, servant=servant, status='completed'
        ).exists()
    return render(request, 'servants/detail.html', {
        'servant': servant, 'reviews': reviews, 'can_review': can_review
    })

@login_required
def servant_register_profile(request):
    if not request.user.is_servant():
        messages.error(request, 'Only servants can access this page.')
        return redirect('home')
    profile = getattr(request.user, 'servant_profile', None)
    if request.method == 'POST':
        form = ServantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            messages.success(request, 'Profile submitted for approval! ✅')
            return redirect('servant_dashboard')
    else:
        form = ServantProfileForm(instance=profile)
    # Build selected_categories list for template checkbox pre-selection
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
    elif profile:
        selected_categories = [str(c.id) for c in profile.categories.all()]
    else:
        selected_categories = []
    return render(request, 'servants/register_profile.html', {
        'form': form,
        'profile': profile,
        'selected_categories': selected_categories,
    })

@login_required
def servant_dashboard(request):
    if not request.user.is_servant():
        return redirect('home')
    profile = getattr(request.user, 'servant_profile', None)
    from bookings.models import Booking
    bookings = Booking.objects.filter(servant=profile).order_by('-created_at') if profile else []
    return render(request, 'servants/dashboard.html', {'profile': profile, 'bookings': bookings})
