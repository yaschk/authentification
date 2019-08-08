from django.contrib import admin
from django.urls import path, include, re_path
from users import views as user_views
from django.contrib.auth import views as auth_views
from users.forms import CustomAuthForm

urlpatterns = [
    #users
    path('admin/', admin.site.urls),
    path('signup/', user_views.signup, name='signup'),
    path('', user_views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('accounts/password_reset/', user_views.reset_password_request_view, name="password_reset"),
    path('accounts/password_reset/username/done/', user_views.password_reset_user, name='password_reset_user'),
    path('accounts/password_reset/phone/done/', user_views.password_reset_phone, name='password_reset_phone'),
    re_path(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', user_views.New_PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/access-banned/', user_views.banned, name='banned'),
    re_path(r'^account_activation_sent/$', user_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            user_views.activate, name='activate'),
    re_path(r'^verification/token/$', user_views.token_validation, name='token_validation'),
    re_path(r'^verified/$', user_views.verified, name='verified'),
    #end users
]
