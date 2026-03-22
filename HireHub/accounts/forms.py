from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# ------------------------------
# Registration Form
# ------------------------------
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'id_username',
            'required': True
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'id': 'id_email',
            'required': True
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'id_password1',
            'required': True
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'id': 'id_password2',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ------------------------------
# Login Form
# ------------------------------
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Email Address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'id': 'id_username',
            'required': True
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'id_password',
            'required': True
        })
    )
    remember_me = forms.BooleanField(
        label="Remember Me",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_remember_me'
        })
    )