from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    name_bn = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=50, default='fa-hands-helping')
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#FF6B6B')

    def __str__(self):
        return self.name

class ServantProfile(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('off', 'Off Duty'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='servant_profile')
    categories = models.ManyToManyField(ServiceCategory, related_name='servants')
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    experience_years = models.PositiveIntegerField(default=0)
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='available')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                  validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.PositiveIntegerField(default=0)
    total_jobs = models.PositiveIntegerField(default=0)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    location = models.CharField(max_length=200, blank=True)
    nid_number = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Servant"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class Review(models.Model):
    servant = models.ForeignKey(ServantProfile, on_delete=models.CASCADE, related_name='reviews')
    hirer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['servant', 'hirer']

    def __str__(self):
        return f"Review by {self.hirer.username} for {self.servant}"
