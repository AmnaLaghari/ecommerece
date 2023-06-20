def not_owner(user, product):
    return user.id != product.owner.id