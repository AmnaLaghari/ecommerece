from django.views.generic import CreateView
from django.contrib import messages
from products.models.product import Products
from products.models.image import Image
from products.forms import ProductForm
from django.urls import reverse_lazy

class CreateProduct(CreateView):
    model = Products
    template_name = 'add_product.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        product = Products.objects.filter(id=self.object.id).first()
        photos = self.request.FILES.getlist('photo')
        if photos:
            for image in photos:
                Image.objects.create(image=image, product= product)
        messages.success(self.request, "Product added successfully")
        return super(CreateProduct, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products')
