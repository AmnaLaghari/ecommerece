from django.views.generic import DeleteView
from products.models.product import Products
from products.models.image import Image
from products.forms import ProductForm
from customusers.utils import not_owner
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class DeleteProduct(DeleteView):
    model = Products
    template_name = 'delete_product.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not_owner(self.request.user, obj):
            messages.error(
                request, "you are not authorized to delete this product")
            redirect('products')
        return super(DeleteProduct, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('products')