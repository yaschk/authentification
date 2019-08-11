from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from users.forms import CustomAuthForm

urlpatterns = [
    path('', user_views.home, name='home'),
    path('admin/', admin.site.urls),

    #users
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', user_views.reset_password_request_view, name="password_reset"),
    path('password-reset/<user>/', user_views.reset_password_with_username,
         name="password_reset_confirm_user"),
    path('password-reset/username/done/', user_views.password_reset_user, name='password_reset_user'),
    path('password-reset/phone/done/', user_views.password_reset_phone, name='password_reset_phone'),
    path('password-reset/email/done/', user_views.password_reset_user, name='password_reset_email'),
    path('password-confirm/<uidb64>/<token>/', user_views.New_PasswordResetConfirmView.as_view(),
         name='reset_password_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('login/banned/', user_views.banned, name='banned'),

    path('account-activation-sent/', user_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('verification/token/', user_views.token_validation, name='token_validation'),
    path('verified/', user_views.verified, name='verified'),
    #end users
]
