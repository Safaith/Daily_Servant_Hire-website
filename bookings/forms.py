from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_date', 'service_address', 'special_instructions']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date', 'min': ''}),
            'service_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Full address where service is needed'}),
            'special_instructions': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any special instructions (optional)'}),
        }
