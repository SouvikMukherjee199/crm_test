from django.contrib import admin
from .models import Client, Product
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at")


admin.site.register(Client, ClientAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("client", "product_name",  "price" )

admin.site.register(Product, ProductAdmin)