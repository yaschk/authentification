from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from users.spec_func import ipInfo, get_calling_code


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignUpForm(UserCreationForm):
    first_and_last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email_or_phone = forms.CharField(max_length=50, label="Phone number or Email", required=True)

    class Meta:
        model = User
        fields = ('email_or_phone', 'username', 'first_and_last_name', 'password1', 'password2', )

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data['email_or_phone']

        try:
            if User.objects.filter(phone=email_or_phone).exists():
                raise ValidationError("Entered phone already exists")
            it_is_normal_phone = True
        except ValueError:
            it_is_normal_phone = False


        if not it_is_normal_phone:
            try:
                if User.objects.filter(phone='+' + email_or_phone).exists():
                    raise ValidationError("Entered phone already exists")
                it_is_plus_phone = True
                email_or_phone = '+' + email_or_phone
            except ValueError:
                it_is_plus_phone = False

            if not it_is_plus_phone:
                try:
                    if User.objects.filter(phone=('+' + str(get_calling_code(ipInfo())) + email_or_phone)).exists():
                        raise ValidationError("Entered phone already exists")
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
                            raise ValidationError("Entered email already exists")
                    else:
                        raise ValidationError("Incorrect field")

        return email_or_phone


class TokenForm(forms.Form):
    token = forms.CharField(max_length=6)


class PasswordResetRequestForm(forms.Form):
    email_or_phone_or_username = forms.CharField(max_length=50, label="Phone number or Email or Username", required=True)

    class Meta:
        model = User
        fields = ('email_or_phone_or_username',)

    def clean_email_or_phone_or_username(self):
        email_or_phone_or_username = self.cleaned_data['email_or_phone_or_username']

        try:
            if User.objects.get(phone=email_or_phone_or_username):
                return email_or_phone_or_username
            it_is_normal_phone = True
        except ValueError:
            it_is_normal_phone = False

        if not it_is_normal_phone:
            try:
                if User.objects.get(phone='+' + email_or_phone_or_username):
                    return '+' + email_or_phone_or_username
                it_is_plus_phone = True
            except ValueError:
                it_is_plus_phone = False

            if not it_is_plus_phone:
                try:
                    if User.objects.get(phone=('+' + str(get_calling_code(ipInfo())) + email_or_phone_or_username)):
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
                            if User.objects.get(email=email_or_phone_or_username):
                                return email_or_phone_or_username
                        elif User.objects.get(username=email_or_phone_or_username):
                            return email_or_phone_or_username
                    except ObjectDoesNotExist:
                        raise ValidationError("This member doesn't exist")


class SetPasswordForm(forms.Form):

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


