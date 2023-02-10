from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile


@admin.register(Profile)
class ModelProfile(admin.ModelAdmin):
    list_display = ['id', 'user_account']
    fieldsets = [
        ('profile_image', {
            'fields': ['profile_image', 'user_account']
        }),
        ('personal_information', {
            'fields': (('nid', 'passport'), 'driver_license')
        }),
        ('account_detail', {
            'fields': [('account_number', 'balance'), 'verified']
        })
    ]
