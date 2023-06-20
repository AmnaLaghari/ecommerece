from django.urls import path
from .views.create_product import CreateProduct
from .views.product_list import ProductList, MyProducts
from .views.product_detail import ProductDetail
from .views.update_product import UpdateProduct
from .views.delete_product import DeleteProduct
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', ProductList.as_view(), name="products"),
    path('my-products/', login_required(MyProducts.as_view(), login_url="login"), name="my_products"),
    path('add-product/', login_required(CreateProduct.as_view(), login_url="login"), name="add_product"),
    path('product/<int:pk>/', login_required(ProductDetail.as_view(), login_url='login'), name='product_detail'),
    path('edit_product/<int:pk>/', login_required(UpdateProduct.as_view(), login_url='login'), name='edit_product'),
    path('delete_product/<int:pk>/', login_required(DeleteProduct.as_view(), login_url='login'), name='delete_product'),

]
