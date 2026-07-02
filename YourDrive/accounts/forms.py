from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserPreference


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        for field in self.fields.values():
            field.help_text = None


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['preferred_brand', 'preferred_fuel_type', 'preferred_transmission', 'min_budget', 'max_budget']
        widgets = {
            'preferred_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Toyota, Honda'}),
            'preferred_fuel_type': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Any'), ('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid'), ('CNG', 'CNG')]),
            'preferred_transmission': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Any'), ('Manual', 'Manual'), ('Automatic', 'Automatic'), ('CVT', 'CVT'), ('DCT', 'DCT')]),
            'min_budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min budget'}),
            'max_budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max budget'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'budget']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
        }
