from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )