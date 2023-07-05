from django.contrib import admin
from .models import CreatorDetails
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(User)
class CreatorDetailModel(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('username', 'email')
