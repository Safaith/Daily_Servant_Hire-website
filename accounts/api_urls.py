from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.login_api, name='api_login'),
    path('logout/', views.logout_api, name='api_logout'),
    path('profile/', views.profile_api, name='api_profile'),
]
