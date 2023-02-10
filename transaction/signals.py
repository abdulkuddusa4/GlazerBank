from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import UploadedFile
import os
from .utils import send_html_mail, MSG_FOR_SENDER, MSG_FOR_RECEPIENT
from user.models import Profile


from GlazerBank import settings
from .utils import get_pdf_obj


@receiver(post_save, sender='transaction.Transaction')
def create_receipt(sender, **kwargs):
    instance = kwargs['instance']

    # let's first disconnect the function to avoid RecursionError
    post_save.disconnect(create_receipt, sender=sender)

    path = settings.BASE_DIR/settings.MEDIA_ROOT/\
        instance.receipt.field.upload_to
    tmp_name = 'temporary_pdf.pdf'
    name = f"receipt_{instance.id}.pdf"

    pdf = get_pdf_obj(
        instance.sender.get_full_name(),
        str(instance.sender.account_number),
        instance.recipient.get_full_name(),
        str(instance.recipient.account_number)
    )
    pdf.output(path/tmp_name, 'F')
    instance.receipt.save(name, UploadedFile(open(path/tmp_name, 'rb')))
    os.remove(path/tmp_name)

    send_html_mail(
        subject='A Transaction Happened',
        msg=MSG_FOR_SENDER.format(
            name=instance.sender.get_full_name(),
            ammount=instance.ammount,
        ),
        recipient=[instance.sender.user_account.email],
        attachments=[instance.receipt.path]
    )

    send_html_mail(
        subject='A Transaction Happened',
        msg=MSG_FOR_RECEPIENT.format(
            name=instance.recipient.get_full_name(),
            ammount=instance.ammount,
            sender=instance.sender.get_full_name(),

        ),
        recipient=[instance.recipient.user_account.email],
        attachments=[instance.receipt.path]
    )

    p = Profile.objects.get(id=instance.sender_id)
    p.balance -= instance.ammount
    p.save()
    # after the job's done connect the function again
    post_save.connect(create_receipt, sender=sender)

