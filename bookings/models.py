from django.db import models
from accounts.models import User
from servants.models import ServantProfile

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]
    hirer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_hirer')
    servant = models.ForeignKey(ServantProfile, on_delete=models.CASCADE, related_name='bookings')
    service_date = models.DateField()
    service_address = models.TextField()
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.hirer.username} -> {self.servant}"

    class Meta:
        ordering = ['-created_at']
