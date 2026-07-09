from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['budget', 'city', 'preferred_fuel_type', 'preferred_transmission', 'preferred_seating', 'phone']
        widgets = {
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_fuel_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Any'), ('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                ('Electric', 'Electric'), ('Hybrid', 'Hybrid'), ('CNG', 'CNG'),
            ]),
            'preferred_transmission': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Any'), ('Manual', 'Manual'), ('Automatic', 'Automatic'), ('CVT', 'CVT'),
            ]),
            'preferred_seating': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
