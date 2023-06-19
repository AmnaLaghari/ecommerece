from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    username = models.CharField(_('Username'), max_length=255,unique=True)
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    profile = CloudinaryField('image', null = True)

    def __str__(self):
        return self.username

    def register(self):
        self.save()