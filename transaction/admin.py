from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('')
    # ]
    fields = ['sender', 'recipient', 'ammount']
