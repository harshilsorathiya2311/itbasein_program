from django import forms
from .models import TestDriveBooking
from cars.models import Car


class BookingForm(forms.ModelForm):
    class Meta:
        model = TestDriveBooking
        fields = ['car', 'booking_date', 'booking_time', 'notes']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].empty_label = 'Select a Car'
