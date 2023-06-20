from django import forms
from django.utils.translation import gettext_lazy as _

from products.models.product import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('title', 'description', 'price', 'quantity')


