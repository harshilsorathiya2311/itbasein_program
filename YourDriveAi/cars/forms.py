from django import forms
from .models import Car

class CarSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search cars...'
    }))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Min price'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Max price'
    }))
    fuel_type = forms.ChoiceField(required=False, choices=[
        ('', 'All Fuels'), ('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
        ('Electric', 'Electric'), ('Hybrid', 'Hybrid'), ('CNG', 'CNG'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    transmission = forms.ChoiceField(required=False, choices=[
        ('', 'All Transmissions'), ('Manual', 'Manual'), ('Automatic', 'Automatic'), ('CVT', 'CVT'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))
