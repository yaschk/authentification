from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from users.forms import SignUpForm, TokenForm, CSetPasswordForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from users.tokens import account_activation_token
from django.contrib.auth import get_user_model
from authy.api import AuthyApiClient
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import *
from users.forms import PasswordResetRequestForm
from django.contrib import messages
from django.db.models.query_utils import Q
import phonenumbers
from users.spec_func import mail_creator_phone, mail_creator_email, validate_email_address
from django.contrib.auth.views import PasswordResetConfirmView

authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            check_email_or_phone = form.cleaned_data['email_or_phone']
            user = form.save(commit=False)
            if '@' in check_email_or_phone:
                user.email = form.cleaned_data['email_or_phone']
                user.unconfirmed_email = user.email
                user.email = None
                user.is_active = False
                user.save()
                try:
                    current_site = get_current_site(request)
                    subject = 'Activate Your MySite Account'
                    message = render_to_string('registration/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message)
                    return redirect('account_activation_sent')
                except:
                    form = SignUpForm()
            else:
                user.phone = form.cleaned_data['email_or_phone']
                user.unconfirmed_phone = user.phone
                user.phone = None
                user.is_active = False
                user.save()
                try:
                    request.session['phone'] = form.cleaned_data['email_or_phone']
                    country_code, national_nmb = phonenumbers.parse(request.session['phone'], None).country_code, phonenumbers.parse(request.session['phone'], None).national_number
                    request.session['userUIDB64'] = urlsafe_base64_encode(force_bytes(user.pk))
                    authy_api.phones.verification_start(
                        national_nmb,
                        country_code,
                        'sms'
                    )
                    return redirect('token_validation')
                except:
                    form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            country_code, national_nmb = phonenumbers.parse(request.session['phone'], None).country_code, phonenumbers.parse(request.session['phone'], None).national_number
            verification = authy_api.phones.verification_check(
                national_nmb,
                country_code,
                form.cleaned_data['token']
            )
            if verification.ok():
                request.session['is_verified'] = True
                return redirect('verified')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'registration/token_validation.html', {'form': form})


def verified(request):
    try:
        uid = force_text(urlsafe_base64_decode(request.session['userUIDB64']))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and request.session.get('is_verified'):
        user.is_active = True
        user.phone_confirmed = True
        user.phone = user.unconfirmed_phone
        user.unconfirmed_phone = None
        user.save()
        login(request, user, backend='users.mybackend.EmailOrUsernameOrPhoneNumberModelBackend')
        return redirect('home')
    else:
        return redirect('signup')


def home(request):
    return render(request, 'landing/home.html', locals())


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.email = user.unconfirmed_email
        user.unconfirmed_email = None
        user.save()
        login(request, user, backend='users.mybackend.EmailOrUsernameOrPhoneNumberModelBackend')
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html', locals())


def banned(request):
    return render(request, 'registration/banned.html')


def password_reset_user(request):
    return render(request, 'registration/password_reset_user_done.html')


def password_reset_phone(request):
    return render(request, 'registration/password_reset_phone_done.html')


def reset_password_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_phone_or_username"]
            # PHONE
            try:
                associated_users = User.objects.filter(Q(phone=data))
                for user in associated_users:
                    mail_creator_phone(user, request)
                return redirect('password_reset_phone')
            # EMAIL
            except ValueError:
                if validate_email_address(data):
                    associated_users = User.objects.filter(Q(email=data) | Q(username=data))
                    for user in associated_users:
                        mail_creator_email(user, request)
                    return redirect('password_reset_done')
            #USERNAME
                else:
                    associated_users = User.objects.filter(username=data)
                    for user in associated_users:
                        if user.email_confirmed:
                            mail_creator_email(user, request)
                        else:
                            mail_creator_phone(user, request)
                    return redirect('password_reset_user')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


# class PasswordResetConfirmView(FormView):
#     template_name = "registration/password_reset_confirm.html"
#     success_url = '/accounts/reset/done/'
#     form_class = SetPasswordForm
#
#     def post(self, request, uidb64=None, token=None, *arg, **kwargs):
#         UserModel = get_user_model()
#         form = self.form_class(request.POST)
#         assert uidb64 is not None and token is not None
#         try:
#             uid = urlsafe_base64_decode(uidb64)
#             user = UserModel._default_manager.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#             user = None
#
#         if user is not None and default_token_generator.check_token(user, token):
#             if form.is_valid():
#                 new_password = form.cleaned_data['new_password2']
#                 user.set_password(new_password)
#                 user.save()
#                 # messages.success(request, 'Password has been reset.')
#                 return self.form_valid(form)
#             else:
#                 # form = SetPasswordForm()
#                 # return render(request, 'registration/password_reset_confirm.html', {'form': form})
#                 # messages.error(request, 'Password reset has not been unsuccessful.')
#                 return self.form_invalid(form)
#         else:
#             messages.error(request, 'The reset password link is no longer valid.')
#             return self.form_invalid(form)

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):


class New_PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CSetPasswordForm
    def __init__(self):
        super(New_PasswordResetConfirmView, self)