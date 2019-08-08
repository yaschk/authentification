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
    username = models.CharField(_('Username'), max_length=10, unique=True)
    first_and_last_name = models.CharField(_('First and last name'), max_length=50, blank=True)
    email = models.EmailField(_('Email'), unique=True, blank=True, null=True)
    phone = PhoneNumberField(_('Phone number'),  unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    is_active = models.BooleanField(_('Active status'), default=True)
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    avatar = models.ImageField(_('Avatar'), upload_to='avatars/', null=True, blank=True)
    email_confirmed = models.BooleanField(_('Email confirmed'), default=False)
    phone_confirmed = models.BooleanField(_('Phone confirmed'), default=False)
    unconfirmed_email = models.EmailField(_('Unconfirmed email'), null=True, blank=True)
    unconfirmed_phone = PhoneNumberField(_('Unconfirmed phone'), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.unconfirmed_email], **kwargs)

