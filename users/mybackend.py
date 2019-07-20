from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameOrPhoneNumberModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        try:
            users = user_model._default_manager.filter(
                Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username, email_confirmed=True) | Q(phone=username, phone_confirmed=True)
            )
        except:
            users = user_model._default_manager.filter(
                Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username, email_confirmed=True)
            )

        for user in users:
            if user.check_password(password):
                user.save()
                return user

        if not users:
            user_model().set_password(password)
