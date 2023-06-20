from django.db import models
from customusers.models import CustomUser
from products.models.product import Products
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.

class Comment(models.Model):
    content = models.CharField(_("content"), max_length=1000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name="comments", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.product.pk})
    
    def __str__(self) -> str:
        return self.content