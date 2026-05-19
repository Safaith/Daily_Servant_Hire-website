from django.urls import path
from . import views
urlpatterns = [
    path('initiate/', views.initiate_payment, name='api_initiate_payment'),
    path('confirm/', views.confirm_payment, name='api_confirm_payment'),
]
