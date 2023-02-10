from django import forms
from .models import Transaction
from user.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from user.models import Profile


class TransactionForm(forms.Form):
    account_number = forms.CharField(max_length=9, required=True)
    ammount = forms.DecimalField(max_digits=25, decimal_places=3, required=True)

    def __init__(self, *args, **kwargs):
        if 'sender_profile' in kwargs:
            self.sender_profile = kwargs.pop('sender_profile')
        super().__init__(*args, **kwargs)

    def clean_account_number(self):
        try:
            account_number = self.cleaned_data.get('account_number')
            recipient = Profile.objects.get(account_number=account_number)
            if recipient.account_number == self.sender_profile.account_number:
                raise forms.ValidationError("Invalid Account Number")
            return recipient
        except ObjectDoesNotExist:
            raise forms.ValidationError("account does'nt exist")
            pass
        pass

    def clean_ammount(self):
        ammount = self.cleaned_data.get('ammount')
        if float(ammount)-3.0 > self.sender_profile.balance:
            raise forms.ValidationError('Insufficient Balance')
        else:
            return ammount

