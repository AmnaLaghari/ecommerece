from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from products.models.product import Products
from django.db.models import Q

class ProductList(ListView):
    model = Products
    template_name = 'products.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Products.objects.filter(~Q(owner = self.request.user))
        else:
            queryset = Products.objects.all()
        return queryset
    
class MyProducts(ListView):
    model = Products
    template_name = 'products.html'

    def get_queryset(self):
        queryset = Products.objects.filter(owner = self.request.user)
        return queryset
    