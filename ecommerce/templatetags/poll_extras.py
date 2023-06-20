from django import template

register = template.Library()

@register.filter(name='is_owner_of_product')
def is_owner_of_product(user, product):
    return user == product.owner