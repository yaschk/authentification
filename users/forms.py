from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(label="Phone number")

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2",)


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(label="Phone number")

    class Meta:
        model = User
        fields = ("username", "email", "phone", )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.CharField(label="Phone number", max_length=15, help_text='Required. Inform a valid phone number.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', )