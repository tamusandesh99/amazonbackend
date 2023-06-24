from django.contrib import admin
from .models import CreaterDetails


# Register your models here.


@admin.register(CreaterDetails)
class CreatorDetailModel(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('username', 'email')
