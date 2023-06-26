from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from products.models.product import Products
from cart.models import Cart, CartItems
from customusers.utils import not_owner, calculate_cart_price

class CustomLoginView(LoginView):
   def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        cart = self.request.session.get('cart')
        if request.user.is_authenticated:
            if cart:
                for key in cart.keys():
                    product = Products.objects.get(pk=key)
                    if not_owner(self.request.user, product):
                        if Cart.get_cart_by_customer(request.user.id):
                            new_cart = Cart.objects.filter(buyer = request.user).first()
                            if product not in new_cart.product.all():
                                CartItems.objects.create(product=product, cart=new_cart, product_quantity=cart[key], product_price=cart[key] * product.price)
                                new_cart.save()
                            else:
                                cart_item = CartItems.objects.filter(product=product, cart=new_cart).first()
                                cart_item.product_quantity += cart[key]
                                cart_item.product_price += (cart[key] * product.price)
                                cart_item.save()
                        else:
                            new_cart = Cart.objects.create(buyer = request.user)
                            CartItems.objects.create(product=product, cart=new_cart, product_quantity=cart[key], product_price=product.price)
                            new_cart.save()
            return redirect('products')
        return response