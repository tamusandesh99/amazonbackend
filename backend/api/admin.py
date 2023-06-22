from django.contrib import admin
from .models import AuthorDetails


# Register your models here.


@admin.register(AuthorDetails)
class AuthorDetailModel(admin.ModelAdmin):
    list_filter = ('firstname', 'lastname')
    list_display = ('firstname', 'lastname')
