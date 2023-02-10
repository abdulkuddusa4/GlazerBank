from django.dispatch import receiver
from django.db.models.signals import post_save
from user.models import Profile
from PIL import Image
from django.core.files.uploadedfile import UploadedFile as File
from django.contrib.auth.models import User


@receiver(post_save, sender='auth.User')
def create_user_profile(sender, **kwargs):
    print("creation")
    user = kwargs['instance']
    try:
        obj = Profile.objects.get(user_account_id=user.id)
    except Profile.DoesNotExist:
        obj = Profile.objects.create(user_account_id=user.id)


@receiver(post_save, sender='auth.User')
@receiver(post_save, sender='user.Profile')
def update_profile(sender, **kwargs):
    if sender==User:
        kwargs['instance'].profile.save()
    else:
        # first disconnect the receiver to avoid recursive signaling
        post_save.disconnect(update_profile, sender=sender)
        profile = kwargs['instance']
        if not profile.account_number:
            profile.account_number = '88' + str(profile.user_account_id).rjust(7, '0')
            pass

        img = Image.open(profile.profile_image.path)
        old_name = profile.profile_image.path.split('/')[-1]

        fmt = old_name.split('.')[-1]

        name = f"image_{profile.user_account.id}.{fmt}"
        if img.width > 300 or img.height > 300:
            img.thumbnail((300, 300))
            print('sdf')
        img.save(profile.profile_image.path)
        obj = open(profile.profile_image.path, 'rb')
        profile.profile_image.save(name, File(open(profile.profile_image.path, 'rb')))

        # after everything is done, connect the function again
        post_save.connect(update_profile, sender=sender)

