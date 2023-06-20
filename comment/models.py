from django.db import models
from customusers.models import CustomUser
from products.models.product import Products
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Comment(models.Model):
    content = models.CharField(_("content"), max_length=1000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name=_(""), on_delete=models.CASCADE)

