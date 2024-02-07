from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CreatorDetails


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'email')


admin.site.register(CreatorDetails, CustomUserAdmin)

