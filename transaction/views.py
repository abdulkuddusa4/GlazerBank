from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from GlazerBank import settings
from .forms import TransactionForm
from .models import Transaction


class BalanceTransfer(View):
    def get(self, request):
        context = {
            'form': TransactionForm()
        }
        return render(request, 'balance_transfer_form.html', context)

    def post(self, request):
        form = TransactionForm(request.POST, sender_profile=request.user.profile)
        context = {
            'form': form,
        }
        if form.is_valid():
            recipient = form.cleaned_data.get('account_number')
            ammount = form.cleaned_data.get('ammount')
            recpt = Transaction(
                sender=request.user.profile,
                recipient=recipient,
                ammount=ammount

            )
            recpt.save()
            return redirect('user-profile')
        else:
            return render(request, 'balance_transfer_form.html', context)

    @classmethod
    def as_view(cls, **initkwargs):
        return login_required(super().as_view())

