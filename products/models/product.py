from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from customusers.models import CustomUser

class Products(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.CharField(_("description"), max_length=1000)
    price = models.IntegerField(_("price"))
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"))

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

