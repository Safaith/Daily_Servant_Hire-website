from django import forms
from .models import ServantProfile, ServiceCategory

class ServantProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=ServiceCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = ServantProfile
        fields = ['categories', 'daily_rate', 'experience_years', 'skills', 'location', 'nid_number']
        widgets = {
            'daily_rate': forms.NumberInput(attrs={'placeholder': 'Daily rate in BDT'}),
            'experience_years': forms.NumberInput(attrs={'min': 0}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. Cooking, Cleaning, Childcare'}),
            'location': forms.TextInput(attrs={'placeholder': 'Your area/district'}),
            'nid_number': forms.TextInput(attrs={'placeholder': 'National ID Number'}),
        }
