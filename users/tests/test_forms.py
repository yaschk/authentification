from django.test import TestCase
import datetime
from django.utils import timezone
from users.forms import CustomAuthForm, SignUpForm


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


    # def test_renew_form_date_field_help_text(self):
    #     form = RenewBookForm()
    #     self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')
    #
    # def test_renew_form_date_in_past(self):
    #     date = datetime.date.today() - datetime.timedelta(days=1)
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertFalse(form.is_valid())
    #
    # def test_renew_form_date_too_far_in_future(self):
    #     date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertFalse(form.is_valid())
    #
    # def test_renew_form_date_today(self):
    #     date = datetime.date.today()
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertTrue(form.is_valid())
    #
    # def test_renew_form_date_max(self):
    #     date = timezone.now() + datetime.timedelta(weeks=4)
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertTrue(form.is_valid())