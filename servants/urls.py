from django.urls import path
from . import views
urlpatterns = [
    path('', views.servant_list_view, name='servant_list'),
    path('<int:pk>/', views.servant_detail_view, name='servant_detail'),
    path('register-profile/', views.servant_register_profile, name='servant_register_profile'),
    path('dashboard/', views.servant_dashboard, name='servant_dashboard'),
]
