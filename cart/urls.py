from django.urls import path
from cart import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('add/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('inc/<int:pk>/', views.increase_quantity, name="inc_quantity"),
    path('dec/<int:pk>/', views.decrease_quantity, name="dec_quantity"),
    path('delete/<int:pk>/', views.delete_form_cart, name="delete_from_cart"),
    path('', views.CartList.as_view(), name="cart_list")
]
