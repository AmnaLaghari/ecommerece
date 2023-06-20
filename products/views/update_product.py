from django.views.generic import UpdateView
from products.models.product import Products
from products.models.image import Image
from products.forms import ProductForm
from customusers.utils import not_owner
from django.shortcuts import redirect
from django.contrib import messages

class UpdateProduct(UpdateView):
    model = Products
    template_name = 'update_product.html'
    form_class = ProductForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not_owner(self.request.user, obj):
            messages.error(request, "you are not authorized to edit this product")
            return redirect('products')
        return super(UpdateProduct, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        product = Products.objects.filter(id=self.object.id).first()
        photos = self.request.FILES.getlist('photo')
        if photos:
            Image.objects.filter(product=product).delete()
            for image in photos:
                Image.objects.create(image=image, product= product)
        messages.success(self.request, "Product updated successfully")
        return super(UpdateProduct, self).form_valid(form)
