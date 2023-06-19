from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from customusers.models import CustomUser

# Create your models here.
class Products(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.CharField(_("description"), max_length=1000)
    price = models.IntegerField(_("price"))
    images = CloudinaryField('image', null = True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"))
