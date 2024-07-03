from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['phone_number', 'iin', 'first_name', 'last_name',]
    search_fields = ('phone_number', 'first_name', 'last_name', 'iin')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'iin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'is_staff', 'is_superuser', 'iin')}
        ),
    )

admin.site.register(User, CustomUserAdmin)