from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from users.forms import SignUpForm, TokenForm, CSetPasswordForm, PasswordResetRequestForm, FullEmailOrPhoneForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.utils.encoding import force_text, force_bytes
from users.tokens import account_activation_token
from authy.api import AuthyApiClient
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
                    country_code, national_nmb = phonenumbers.parse(request.session['phone'],
                                                                    None).country_code, phonenumbers.parse(
                        request.session['phone'], None).national_number
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
            country_code, national_nmb = phonenumbers.parse(request.session['phone'],
                                                            None).country_code, phonenumbers.parse(
                request.session['phone'], None).national_number
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
                    return redirect('password_reset_email')
                # USERNAME
                else:
                    associated_users = User.objects.filter(username=data)
                    for user in associated_users:
                        return redirect('password_reset_confirm_user', user)

    else:
        form = PasswordResetRequestForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


def reset_password_with_username(request, user):
    try:
        curr_user = User.objects.filter(username=user)[0]
        encode_email, encode_phone = None, None
        if curr_user.email_confirmed:
            part_email = str(curr_user.email).split('@')
            encode_email = part_email[0][:-round(len(part_email[0]) / 2)] + '*' * round(
                len(part_email[0]) / 2) + '@' + \
                           part_email[1]
        elif curr_user.phone_confirmed:
            encode_phone = str(curr_user.phone)[:-5] + '****' + str(curr_user.phone)[-1:]
        if request.method == 'POST':
            form = FullEmailOrPhoneForm(data=request.POST, user=curr_user)
            if form.is_valid():
                if encode_email is not None:
                    mail_creator_email(curr_user, request)
                    return redirect('password_reset_user')
                else:
                    mail_creator_phone(curr_user, request)
                    return redirect('password_reset_phone')
        else:
                form = FullEmailOrPhoneForm(user=curr_user)
        return render(request, 'registration/password_reset_with_username.html', {'form': form,
                                                                              'encode_email': encode_email,
                                                                              'encode_phone': encode_phone},)
    except IndexError:
        return redirect('password_reset')


class New_PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CSetPasswordForm

    def __init__(self):
        super(New_PasswordResetConfirmView, self)
