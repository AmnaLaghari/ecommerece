from django.db import models
from .product import Products
from cloudinary.models import CloudinaryField

class Image(models.Model):
    image = CloudinaryField('image', null = True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)