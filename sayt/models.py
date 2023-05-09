from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CastomUserManager(BaseUserManager):
    def create_user(self, gmail, password, is_staff=False, is_active=True, is_superuser=True, *args, **kwargs):
        user = self.model(gmail=gmail,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, gmail, password, is_staff=True, is_active=True, is_superuser=True, *args, **kwargs):
        return self.create_user(gmail=gmail,
                                password=password,
                                is_staff=is_staff,
                                is_active=is_active,
                                is_superuser=is_superuser,
                                **kwargs)


class User(AbstractUser):
    name = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gmail = models.CharField(max_length=128, unique=True, null=True, blank=True)
    password = models.CharField(_('password'), max_length=256)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    username = False
    objects = CastomUserManager()

    USERNAME_FIELD = 'gmail'

    REQUIRED_FIELDS = []

    def res(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "gmail": self.gmail,
            "password": self.password,

        }


class OTP(models.Model):
    key = models.CharField(max_length=990)
    gmail = models.CharField(max_length=128)
    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    state = models.CharField(max_length=25)
    is_comfirmed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    update_at = models.DateTimeField(auto_now_add=False, auto_now=True, )

    def save(self, *args, **kwargs):
        if self.is_expired >= 3:
            self.is_expired = True
        return super(OTP, self).save(*args, **kwargs)
