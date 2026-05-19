from django.urls import path
from . import views
from servants.serializers import ServiceCategorySerializer
from servants.models import ServiceCategory
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    cats = ServiceCategory.objects.all()
    return Response(ServiceCategorySerializer(cats, many=True).data)

urlpatterns = [
    path('', views.ServantListAPIView.as_view(), name='api_servant_list'),
    path('<int:pk>/', views.ServantDetailAPIView.as_view(), name='api_servant_detail'),
    path('<int:servant_id>/review/', views.submit_review, name='api_submit_review'),
    path('categories/', category_list, name='api_categories'),
]
