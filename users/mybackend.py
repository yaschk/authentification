from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.spec_func import ipInfo, get_calling_code, check_phone


class EmailOrUsernameOrPhoneNumberModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        it_is_normal_phone = check_phone(username, user_model)
        it_is_plus_phone = check_phone('+' + username, user_model)
        it_is_locale_phone = check_phone(str('+' + str(get_calling_code(ipInfo())) + username), user_model)

        if it_is_normal_phone[0]:
            users = it_is_normal_phone[1]
        elif it_is_plus_phone[0]:
            users = it_is_plus_phone[1]
        elif it_is_locale_phone[0]:
            users = it_is_locale_phone[1]
        else:
            users = user_model._default_manager.filter(Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username, email_confirmed=True))

        for user in users:
            if user.check_password(password):
                user.save()
                return user

        if not users:
            user_model().set_password(password)
