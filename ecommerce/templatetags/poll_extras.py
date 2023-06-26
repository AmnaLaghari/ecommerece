from django import template
from products.models.product import Products
from cart.models import Cart

register = template.Library()

@register.filter(name='is_owner_of_product')
def is_owner_of_product(user, product):
    return user == product.owner

@register.filter(name='item_in_cart')
def item_in_cart(product_id, request):
    user = request.user
    if user.is_authenticated:
        if Cart.get_cart_by_customer(user.id):
            product = Products.objects.get(pk=product_id)
            cart = Cart.objects.filter(buyer = user).first()
            return True if product in cart.product.all() else False
        else:
            return False
    else:
        cart = request.session.get('cart')
        if cart:
            return True if str(product_id) in cart.keys() else False
        else:
            return False
            
@register.filter(name="get_product_quantity")
def get_product_quantity(cart_item, product):
    return cart_item.filter(product=product).first().product_quantity

@register.filter(name="get_product_price")
def get_product_price(cart_item, product):
    return cart_item.filter(product=product).first().product_price

@register.filter(name="get_product_by_id")
def get_product_by_id(id):
    return Products.objects.get(pk=id)

@register.filter(name="get_total_price")
def get_total_price(product, quantity):
    return product.price * quantity

@register.filter(name="get_cart_price")
def get_cart_price(cart, user):
    if user.is_authenticated:
        sum = 0
        for cart_item in cart.cart_items.filter(cart=cart):
            sum = sum + cart_item.product_price
        return sum
    else:
        sum = 0
        for key in cart.keys():
            product = Products.objects.get(pk=key)
            sum = sum + (product.price * cart[key])
        return sum
