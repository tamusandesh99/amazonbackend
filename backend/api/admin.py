from django.contrib import admin
from .models import CreaterDetails


# Register your models here.


@admin.register(CreaterDetails)
class CreatorDetailModel(admin.ModelAdmin):
    list_filter = ('firstname', 'lastname')
    list_display = ('firstname', 'lastname')
