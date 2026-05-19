from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from servants.models import ServantProfile, ServiceCategory
from bookings.models import Booking

def home(request):
    categories = ServiceCategory.objects.all()
    featured_servants = ServantProfile.objects.filter(is_approved=True, availability_status='available').order_by('-rating')[:6]
    stats = {
        'total_servants': ServantProfile.objects.filter(is_approved=True).count(),
        'total_bookings': Booking.objects.filter(status='completed').count(),
        'total_categories': categories.count(),
    }
    return render(request, 'home.html', {'categories': categories, 'featured_servants': featured_servants, 'stats': stats})

def admin_dashboard(request):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.role == 'admin'):
        from django.shortcuts import redirect
        return redirect('login')
    from accounts.models import User
    context = {
        'total_users': User.objects.count(),
        'total_servants': ServantProfile.objects.count(),
        'pending_servants': ServantProfile.objects.filter(is_approved=False).count(),
        'approved_servants': ServantProfile.objects.filter(is_approved=True).count(),
        'total_bookings': Booking.objects.count(),
        'completed_bookings': Booking.objects.filter(status='completed').count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'pending_servant_list': ServantProfile.objects.filter(is_approved=False).select_related('user'),
        'recent_bookings': Booking.objects.select_related('hirer', 'servant__user').order_by('-created_at')[:10],
        'all_users': User.objects.order_by('-date_joined')[:20],
    }
    return render(request, 'admin_panel/dashboard.html', context)

def approve_servant(request, pk):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    from django.shortcuts import redirect
    from servants.models import ServantProfile
    servant = ServantProfile.objects.get(pk=pk)
    servant.is_approved = True
    servant.user.is_verified = True
    servant.user.save()
    servant.save()
    from django.contrib import messages
    messages.success(request, f'{servant.user.get_full_name()} approved as servant! ✅')
    return redirect('admin_dashboard')

urlpatterns = [
    path('', home, name='home'),
    path('django-admin/', admin.site.urls),
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    path('admin-panel/approve-servant/<int:pk>/', approve_servant, name='approve_servant'),
    path('accounts/', include('accounts.urls')),
    path('servants/', include('servants.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
    # REST API
    path('api/accounts/', include('accounts.api_urls')),
    path('api/servants/', include('servants.api_urls')),
    path('api/bookings/', include('bookings.api_urls')),
    path('api/payments/', include('payments.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
