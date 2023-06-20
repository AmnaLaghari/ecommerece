from django.contrib import messages
from django.views.generic import CreateView
from comment.models import Comment
from django.urls import reverse_lazy
from products.models.product import Products
from django.shortcuts import redirect
from comment.forms import CommentForm

class AddComment(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentForm
    reverse_lazy('products')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = Products.objects.get(pk=self.kwargs.get('product_id'))
        return super(AddComment, self).form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        product = Products.objects.get(pk=self.kwargs.get('product_id'))
        if request.user == product.owner:
            messages.error(self.request, "You cannot add comment on yor own product")
            return redirect('post_detail', product.id)
        return super().dispatch(request, *args, **kwargs)