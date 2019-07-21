from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from django.db.models import Q
from authentification import settings
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from authentification.settings import DEFAULT_FROM_EMAIL
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from twilio.rest import Client


def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    data = load(urlopen(url))
    return data['country']


def get_calling_code(iso):
  for code, isos in COUNTRY_CODE_TO_REGION_CODE.items():
    if iso.upper() in isos:
        return code
  return None


def check_phone(username, user_model):
    try:
        return (True, user_model._default_manager.filter(Q(phone=username, phone_confirmed=True)))
    except:
        return (False, None)


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def mail_creator_email(user, request):
    c = {
        'email': user.email,
        'domain': request.META['HTTP_HOST'],
        'site_name': settings.SITE_NAME,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    subject_template_name = 'registration/password_reset_subject.txt'
    email_template_name = 'registration/password_reset_email.html'
    subject = loader.render_to_string(subject_template_name, c)
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string(email_template_name, c)
    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def mail_creator_phone(user, request):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    c = {
        'domain': request.META['HTTP_HOST'],
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    email_template_name = 'registration/password_reset_phone.html'
    email = loader.render_to_string(email_template_name, c)
    message = client.messages \
        .create(
        body=email,
        from_=settings.TWILIO_PHONE_NMB,
        to=user.phone.as_e164
    )