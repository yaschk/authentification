from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, SetPasswordForm
from users.models import CustomUser
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from users.spec_func import ipInfo, get_calling_code
from django.forms.widgets import PasswordInput, TextInput
import string


User = get_user_model()


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label='Username, email or phone number', widget=TextInput(attrs={
                                                                 'class': 'validate, login-input-field',
                                                                 'placeholder': 'Username, email or phone number'}))
    password = forms.CharField(label='Password', widget=PasswordInput(attrs={'class': 'login-input-field',
                                                                             'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignUpForm(UserCreationForm):
    email_or_phone = forms.CharField(max_length=50, label="Email or phone number", required=True,
                                     widget=TextInput(attrs={'placeholder': 'Email or phone number'}))
    first_and_last_name = forms.CharField(max_length=50, label="Full name", required=False, widget=TextInput(attrs={
        'placeholder': 'Full name'}))
    username = forms.CharField(min_length=3, label='Username', widget=TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(min_length=6, label='Password', widget=PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        del self.fields['password2']

    class Meta:
        model = User
        fields = ('email_or_phone', 'username', 'first_and_last_name', 'password1',)

    def clean_username(self):
        username = self.cleaned_data['username']
        allowed_chars = string.ascii_letters + string.digits + '_-.'
        allowed_set = set(allowed_chars)

        def check_set_diff(s):
            return not set(s) - allowed_set

        if User.objects.filter(username=username).exists():
            raise ValidationError("Entered username already exists")

        if len(username) < 3:
            raise ValidationError("Entered username too short. Minimum length is 3 symbols")

        if len(username) > 10:
            raise ValidationError("Entered username too long. Maximum length is 10 symbols")

        if username.isnumeric():
            raise ValidationError("Username can not consist only of numbers")

        if not check_set_diff(username):
            raise ValidationError("Only alphanumeric characters, underscores, and periods can be used in usernames")

        return username

    def clean_password1(self):
        password = self.cleaned_data['password1']

        if len(password) < 6:
            raise ValidationError("The minimum password length is 6 characters")

        if password.isnumeric():
            raise ValidationError("The password can not be only numbers")
        return password

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data['email_or_phone']

        try:
            if User.objects.filter(phone=email_or_phone).exists():
                raise ValidationError("Entered phone already exists 1")
            it_is_normal_phone = True
        except ValueError:
            it_is_normal_phone = False

        if not it_is_normal_phone:
            try:
                if User.objects.filter(phone='+' + email_or_phone).exists():
                    raise ValidationError("Entered phone already exists 2")
                it_is_plus_phone = True
                email_or_phone = '+' + email_or_phone
            except ValueError:
                it_is_plus_phone = False

            if not it_is_plus_phone:
                try:
                    if User.objects.filter(phone=('+' + str(get_calling_code(ipInfo())) + email_or_phone)).exists():
                        print('+' + str(get_calling_code(ipInfo())) + email_or_phone)
                        raise ValidationError("Entered phone already exists 3")
                    it_is_local_phone = True
                    email_or_phone = '+' + str(get_calling_code(ipInfo())) + email_or_phone
                except ValueError:
                    it_is_local_phone = False

                if not it_is_local_phone:
                    try:
                        validate_email(email_or_phone)
                        it_is_email = True
                    except ValidationError:
                        it_is_email = False
                    if it_is_email:
                        if User.objects.filter(email=email_or_phone).exists():
                            raise ValidationError("Entered email already exists 4")
                    else:
                        raise ValidationError("Incorrect field")

        return email_or_phone


class TokenForm(forms.Form):
    token = forms.CharField(max_length=6)


class PasswordResetRequestForm(forms.Form):
    email_or_phone_or_username = forms.CharField(max_length=50, label="Email, username or phone number",
                                                 required=True,
                                                 widget=TextInput(attrs={
                                                     'placeholder': 'Email, username or phone number'}))

    class Meta:
        model = User
        fields = ('email_or_phone_or_username',)

    def clean_email_or_phone_or_username(self):
        email_or_phone_or_username = self.cleaned_data['email_or_phone_or_username']

        try:
            if User.objects.get(phone=email_or_phone_or_username, phone_confirmed=True):
                return email_or_phone_or_username
            it_is_normal_phone = True
        except ValueError:
            it_is_normal_phone = False

        if not it_is_normal_phone:
            try:
                if User.objects.get(phone='+' + email_or_phone_or_username, phone_confirmed=True):
                    return '+' + email_or_phone_or_username
                it_is_plus_phone = True
            except ValueError:
                it_is_plus_phone = False

            if not it_is_plus_phone:
                try:
                    if User.objects.get(phone=('+' + str(get_calling_code(ipInfo())) + email_or_phone_or_username),
                                        phone_confirmed=True):
                        return '+' + str(get_calling_code(ipInfo())) + email_or_phone_or_username
                    it_is_local_phone = True
                except ValueError:
                    it_is_local_phone = False

                if not it_is_local_phone:
                    try:
                        validate_email(email_or_phone_or_username)
                        it_is_email = True
                    except ValidationError:
                        it_is_email = False
                    try:
                        if it_is_email:
                            if User.objects.get(email=email_or_phone_or_username, email_confirmed=True):
                                return email_or_phone_or_username
                        elif User.objects.get(username=email_or_phone_or_username, phone_confirmed=True)\
                                or User.objects.get(username=email_or_phone_or_username, email_confirmed=True):
                            return email_or_phone_or_username
                    except ObjectDoesNotExist:
                        raise ValidationError("This member doesn't exist")


class CSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'New password'}),
        strip=False,

    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'New password confirmation'}),
    )


class FullEmailOrPhoneForm(forms.Form):
    email_or_phone = forms.CharField(max_length=50, label="Email or phone number", required=True,
                                     widget=TextInput(attrs={'placeholder': 'Enter here'}))

    class Meta:
        model = User
        fields = ('email_or_phone',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data['email_or_phone']
        if email_or_phone == self.user.email or email_or_phone == self.user.phone:
            return email_or_phone
        else:
            raise ValidationError("User doesn't exist")
