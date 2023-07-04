from django.shortcuts import redirect
from products.models.product import Products
from cart.models import Cart, CartItems
from django.views.generic import ListView
from customusers.utils import not_owner, calculate_cart_price
from django.contrib import messages
from django.conf import settings 
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.generic.base import TemplateView


def add_to_cart(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user.is_authenticated:
        if not_owner(request.user, product):
            if Cart.get_cart_by_customer(request.user.id):
                cart = Cart.objects.filter(buyer = request.user).first()
                if product not in cart.product.all():
                    CartItems.objects.create(product=product, cart=cart, product_quantity=1, product_price=product.price)
                cart = calculate_cart_price(cart)
                cart.save()
            else:
                new_cart = Cart.objects.create(buyer = request.user)
                CartItems.objects.create(product=product, cart=new_cart, product_quantity=1, product_price=product.price)
                new_cart = calculate_cart_price(new_cart)
                new_cart.save()
            messages.success(request, 'Product added to cart successfully')
        else:
            messages.error(request, "You cannot add this product in the cart.")  
    else:
        cart = request.session.get('cart')
        if cart:
            if str(pk) not in cart.keys():
                cart[f'{pk}'] = 1
                request.session['cart'] = cart

        else:
            request.session['cart'] = {
                f'{pk}':1
            }
        messages.success(request, 'Product added to cart successfully')
            
    return redirect('product_detail', pk)

def increase_quantity(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user.is_authenticated:
        if not_owner(request.user, product):
            if Cart.get_cart_by_customer(request.user.id):
                cart = Cart.get_cart_by_customer(request.user.id).first()
                if product in cart.product.all():
                    cart_item = cart.cart_items.filter(product=product).first()
                    cart_item.product_quantity = cart_item.product_quantity +1
                    cart_item.product_price += product.price
                    cart_item.save()
                    cart = calculate_cart_price(cart)
                    cart.save()
        else:
            messages.error(request, "You cannot add this product in the cart.")  
    else:
        cart = request.session.get('cart')
        if cart:
            if str(pk) in cart.keys():
                cart[str(pk)] += 1
                request.session['cart'] = cart
    return redirect('product_detail', pk)

def decrease_quantity(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user.is_authenticated:
        if not_owner(request.user, product):
            cart = Cart.get_cart_by_customer(request.user.id).first()
            if product in cart.product.all():
                cart_item = cart.cart_items.filter(product=product).first()
                cart_item.product_quantity -= 1
                cart_item.product_price -= product.price
                cart_item.save()
                if cart_item.product_quantity <=  0:
                    delete_form_cart(request, pk)
                cart = calculate_cart_price(cart)
                cart.save()

        else:
            messages.error(request, "You cannot add this product in the cart.") 
    else:
        cart = request.session.get('cart')
        if cart:
            if str(pk) in cart.keys():
                cart[str(pk)] -= 1
                request.session['cart'] = cart
                if cart[str(pk)] <= 0:
                    delete_form_cart(request, pk)
    return redirect('product_detail', product.id)

def delete_form_cart(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user.is_authenticated:
        if Cart.get_cart_by_customer(request.user.id):
            cart = Cart.get_cart_by_customer(request.user.id).first()
            if product in cart.product.all():
                cart.product.remove(product)
                cart = calculate_cart_price(cart)
                cart.save()
                messages.success(request, 'product delete from cart')
    else:
        cart = request.session.get('cart')
        if cart:
            if str(pk) in cart.keys():
                del cart[str(pk)]
                request.session['cart'] = cart
                messages.success(request, 'product delete from cart')
    return redirect('product_detail', product.id)

class CartList(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        if self.request.user.is_authenticated:   
            queryset = Cart.get_cart_by_customer(self.request.user.id).first()
        else:
            queryset = self.request.session.get('cart')
        return queryset
    

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items_list = []
        cart = Cart.objects.filter(buyer = request.user).first()
        for cart_item in cart.cart_items.filter(cart=cart):
            line_items_list.append({
                    'quantity': cart_item.product_quantity * 100, 
                    'price_data': {
                        'unit_amount': cart_item.product.price, 
                        'product_data': {
                            'name': cart_item.product.title,
                        },
                        'currency': 'usd'
                    }
                })
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items_list
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'ecommerce/templates/cancelled.html'

