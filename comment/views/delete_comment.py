from django.contrib import messages
from django.views.generic import DeleteView
from comment.models import Comment
from django.urls import reverse_lazy
from products.models.product import Products
from django.shortcuts import redirect
from comment.forms import CommentForm

class DeleteComment(DeleteView):
    model = Comment
    template_name = 'delete_comment.html'
    reverse_lazy('products')
    
    def dispatch(self, request, *args, **kwargs):
        product = Products.objects.get(pk=self.kwargs.get('product_id'))
        if request.user != product.owner:
            messages.error(self.request, "You are not authorized to delete this post")
            return redirect('post_detail', product.id)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('my_products')