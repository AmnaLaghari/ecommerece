from django.db import models
from products.models.product import Products
from customusers.models import CustomUser
from django.utils.translation import gettext_lazy as _

class CartItems(models.Model):
    product = models.ForeignKey(Products, related_name='cart_items', on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart', related_name='cart_items', on_delete=models.CASCADE)
    product_price = models.IntegerField(_("product_price"))
    product_quantity = models.IntegerField(_("product_quantity"))

# Create your models here.
class Cart(models.Model):
    product = models.ManyToManyField(Products, through='cart.CartItems', related_name='carts')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.IntegerField(_("price"), null=True)

    @staticmethod
    def get_cart_by_customer(buyer_id):
        return Cart.objects.filter(buyer=buyer_id)
