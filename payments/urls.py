from django.urls import path
from . import views
urlpatterns = [
    path('<int:booking_id>/', views.payment_view, name='payment'),
    path('<int:booking_id>/success/', views.payment_success, name='payment_success'),
]
