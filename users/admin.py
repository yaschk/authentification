from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'phone', 'is_staff', 'is_superuser', 'email_confirmed', 'is_active',]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.add_fieldsets[0][1]['fields'] = ('username', 'phone', 'email', 'password1', 'password2',)


admin.site.register(CustomUser, CustomUserAdmin)
