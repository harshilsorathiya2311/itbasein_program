from django import forms
from .models import Car


class CarSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search cars...'
    }))
    brand = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Min price'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'Max price'
    }))
    fuel_type = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    transmission = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    seats = forms.IntegerField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Brand
        brand_choices = [('', 'All Brands')] + [(b.name, b.name) for b in Brand.objects.all()]
        self.fields['brand'].choices = brand_choices
        self.fields['fuel_type'].choices = [('', 'All Fuels'), ('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid')]
        self.fields['transmission'].choices = [('', 'All Transmissions'), ('Manual', 'Manual'), ('Automatic', 'Automatic'), ('CVT', 'CVT'), ('DCT', 'DCT')]
        self.fields['seats'].choices = [('', 'Any Seats')] + [(i, str(i)) for i in [2, 4, 5, 6, 7, 8]]
