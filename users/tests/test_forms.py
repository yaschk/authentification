from django.test import TestCase
from users.forms import CustomAuthForm, SignUpForm, PasswordResetRequestForm


class CustomAuthFormTest(TestCase):

    def test_username_field_label(self):
        form = CustomAuthForm()
        self.assertTrue(form.fields['username'].label == 'Username, email or phone number')

    def test_password_field_label(self):
        form = CustomAuthForm()
        self.assertTrue(form.fields['password'].label == 'Password')

    def test_username_field_placeholder(self):
        form = CustomAuthForm()
        self.assertTrue(form.fields['username'].widget.attrs["placeholder"] == 'Username, email or phone number')

    def test_password_field_placeholder(self):
        form = CustomAuthForm()
        self.assertTrue(form.fields['password'].widget.attrs["placeholder"] == 'Password')


class SignUpFormTest(TestCase):

    def test_email_or_phone_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['email_or_phone'].label == 'Email or phone number')

    def test_first_and_last_name_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['first_and_last_name'].label == 'Full name')

    def test_username_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_password1_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['password1'].label == 'Password')

    def test_username_length_less(self):
        form_data = {'username': 're'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_length_more(self):
        form_data = {'username': 'rewefwefwefewfwef32342fefwefr2fefe2effdsvdfsferf3j43fjn3j'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_is_numeric(self):
        form_data = {"username": "123456"}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_symbols(self):
        form_data = {'username': 'qwerty12@/*+-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_password_length_less(self):
        form_data = {'password1': 're12'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_password_is_numeric(self):
        form_data = {"password1": "123456"}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_or_phone_is_phone(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': '+380987654321'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_or_phone_is_phone_without_plus(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': '380987654321'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_or_phone_is_phone_without_country_code(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': '0987654321'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_or_phone_is_email(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': 'test@gmail.com'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_email_or_phone_is_false(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': '@testgmail.com'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_or_phone_is_phone_without_startzero(self):
        form_data = {'username': 'usr12', 'password1': 'qwerty12034', 'email_or_phone': '987654321'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())


class PasswordResetRequestFormTest(TestCase):

    def test_email_or_phone_or_username_field_label(self):
        form = PasswordResetRequestForm()
        self.assertTrue(form.fields['email_or_phone_or_username'].label == 'Email, username or phone number')

    def test_email_or_phone_or_username_field_placeholder(self):
        form = PasswordResetRequestForm()
        self.assertTrue(form.fields['email_or_phone_or_username'].widget.attrs["placeholder"] ==
                        'Email, username or phone number')
