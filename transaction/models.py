from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from GlazerBank import settings
from user.models import Profile


class Transaction(models.Model):
    sender = models.ForeignKey('user.Profile', on_delete=models.CASCADE,
                               related_name='balanced_transferred')
    recipient = models.ForeignKey('user.Profile', on_delete=models.CASCADE,
                                  related_name='balanced_received')
    ammount = models.DecimalField(decimal_places=3, max_digits=25)
    receipt = models.FileField(upload_to='receipts', null=True)
    date = models.DateTimeField(auto_now=True)

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):




