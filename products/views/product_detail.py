from django.views.generic import DetailView
from products.models.product import Products

class ProductDetail(DetailView):
    context_object_name = 'product'
    model = Products
    template_name = 'product_detail.html'