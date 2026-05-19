from django.urls import path
from . import views
urlpatterns = [
    path('', views.BookingListAPIView.as_view(), name='api_booking_list'),
    path('create/', views.BookingCreateAPIView.as_view(), name='api_booking_create'),
    path('<int:pk>/status/', views.update_booking_status, name='api_booking_status'),
]
