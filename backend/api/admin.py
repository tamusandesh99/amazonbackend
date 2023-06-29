from django.contrib import admin
from .models import CreatorDetails


@admin.register(CreatorDetails)
class CreatorDetailModel(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('username', 'email')
