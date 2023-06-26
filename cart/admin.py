from django.contrib import admin
from .models import Cart,CartItems

# Register your models here.
@admin.register(Cart)
class cartAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItems)
class cartItemsAdmin(admin.ModelAdmin):
    pass