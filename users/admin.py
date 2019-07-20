from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


class UserAdmin(UserAdmin):

    list_display = ['username', 'email', 'phone', 'first_and_last_name', 'is_active', 'is_staff',
                    'email_confirmed', 'phone_confirmed', 'is_superuser', 'unconfirmed_email', 'unconfirmed_phone',]
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_and_last_name', )}),
        ('Permissions', {'fields': ('is_active', 'email_confirmed', 'phone_confirmed', 'is_staff', 'is_superuser', 'groups',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )
    readonly_fields = ('last_login', 'date_joined',)
    list_editable = ('is_active', 'is_staff', )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'), }),)
    search_fields = ['username', 'email', 'phone', 'first_and_last_name', ]

    class Meta:
        model = CustomUser


admin.site.register(CustomUser, UserAdmin)
