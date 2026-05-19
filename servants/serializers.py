from rest_framework import serializers
from .models import ServantProfile, ServiceCategory, Review
from accounts.serializers import UserProfileSerializer

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    hirer_name = serializers.CharField(source='hirer.get_full_name', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'hirer_name', 'rating', 'comment', 'created_at']

class ServantProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    categories = ServiceCategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ServiceCategory.objects.all(), write_only=True, source='categories'
    )
    reviews = ReviewSerializer(many=True, read_only=True)
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = ServantProfile
        fields = ['id', 'user', 'categories', 'category_ids', 'daily_rate', 'experience_years',
                  'availability_status', 'rating', 'total_reviews', 'total_jobs', 'skills',
                  'skills_list', 'location', 'is_approved', 'reviews', 'created_at']
        read_only_fields = ['rating', 'total_reviews', 'total_jobs', 'is_approved']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

class ServantListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    categories = ServiceCategorySerializer(many=True, read_only=True)
    class Meta:
        model = ServantProfile
        fields = ['id', 'user', 'categories', 'daily_rate', 'experience_years',
                  'availability_status', 'rating', 'total_reviews', 'total_jobs', 'location', 'is_approved']
