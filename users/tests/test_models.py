from django.test import TestCase
from users.models import CustomUser


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='BigYaschk123')

    def test_username_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'Username')

    def test_first_and_last_name_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('first_and_last_name').verbose_name
        self.assertEquals(field_label, 'First and last name')

    def test_email_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'Email')

    def test_phone_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'Phone number')

    def test_date_joined_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('date_joined').verbose_name
        self.assertEquals(field_label, 'Date joined')

    def test_is_active_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('is_active').verbose_name
        self.assertEquals(field_label, 'Active status')

    def test_is_staff_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('is_staff').verbose_name
        self.assertEquals(field_label, 'Staff status')

    def test_avatar_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('avatar').verbose_name
        self.assertEquals(field_label, 'Avatar')

    def test_email_confirmed_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('email_confirmed').verbose_name
        self.assertEquals(field_label, 'Email confirmed')

    def test_phone_confirmed_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('phone_confirmed').verbose_name
        self.assertEquals(field_label, 'Phone confirmed')

    def test_unconfirmed_email_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('unconfirmed_email').verbose_name
        self.assertEquals(field_label, 'Unconfirmed email')

    def test_unconfirmed_phone_label(self):
        user = CustomUser.objects.get(id=1)
        field_label = user._meta.get_field('unconfirmed_phone').verbose_name
        self.assertEquals(field_label, 'Unconfirmed phone')

