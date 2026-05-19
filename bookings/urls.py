from django.urls import path
from . import views
urlpatterns = [
    path('book/<int:servant_id>/', views.book_servant, name='book_servant'),
    path('hirer-dashboard/', views.hirer_dashboard, name='hirer_dashboard'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('respond/<int:pk>/', views.servant_respond_booking, name='servant_respond_booking'),
]
