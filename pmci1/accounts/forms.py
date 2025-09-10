from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, StudentRecord

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

class AddUserform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'role': forms.Select(attrs={'placeholder': 'Role'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.set_password(self.cleaned_data['password'])

        # Automatically set staff status if role is admin
        if user.role == 'admin':
            user.is_staff = True
        else:
            user.is_staff = False

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].empty_label = "Select Role"

class StudentRecordForm(forms.ModelForm):
    class Meta:
        model = StudentRecord
        fields = ['lrn', 'last_name', 'first_name', 'middle_name']

    def clean_lrn(self):
        lrn = self.cleaned_data['lrn']
        if not lrn.isdigit():
            raise forms.ValidationError("LRN must contain numbers only.")
        if len(lrn) != 12:
            raise forms.ValidationError("LRN must be exactly 12 digits.")
        return lrn
