from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files import File


class Profile(models.Model):
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=9, null=True, blank=True, unique=True)
    profile_image = models.ImageField(upload_to='profile_images', default='default_image.png',)
    nid = models.CharField(max_length=100, null=True)
    passport = models.CharField(max_length=100, null=True,)
    driver_license = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)
    balance = models.DecimalField(default=0, decimal_places=3, max_digits=25)
    # created_on = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.user_account.first_name}_{self.user_account.last_name}"

    def __str__(self):
        return str(self.user_account)

    # def save(self):
    #     super().save()
    #
    #     if not self.account_number:
    #         self.account_number = '88'+str(self.user_account_id).rjust(7, '0')
    #         pass
    #
    #     img = Image.open(self.profile_image.path)
    #     path = self.profile_image.path.split('/')
    #     fmt = path[-1].split('.')[-1]
    #     path = '/'.join(path[:-1])
    #     name = f"image_{self.user_account.id}.{fmt}"
    #     new_path = path + f"/{name }"
    #     if img.width>300 or img.height>300:
    #         img.thumbnail((300, 300))
    #     img.save(new_path)

        # super().save()

