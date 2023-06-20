from django.contrib import admin
from products.models.product import Products
from products.models.image import Image

# Register your models here.
@admin.register(Products)
class productsAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class imageAdmin(admin.ModelAdmin):
    pass