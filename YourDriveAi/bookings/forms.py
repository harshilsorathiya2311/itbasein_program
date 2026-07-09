from django import forms
from .models import Booking, Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'dealership', 'phone_number', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'dealership': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred dealership'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +1 234 567 890'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}, choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }
