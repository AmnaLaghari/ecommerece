def not_owner(user, product):
    return user.id != product.owner.id

def calculate_cart_price(cart):
    cart.price = 0
    for cart_item in cart.cart_items.filter(cart=cart):
        cart.price = cart.price + cart_item.product_price
    return cart