from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=31, unique=True)
    first_and_last_name = models.CharField(_('name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    phone_confirmed = models.BooleanField(default=False)
    unconfirmed_email = models.EmailField(_('unconfirmed email address'), blank=True, null=True)
    unconfirmed_phone = PhoneNumberField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.first_and_last_name

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_and_last_name.split(' ')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.unconfirmed_email], **kwargs)

