from django.contrib import admin
from .models import Category, Product, ProductImage

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]
    list_display = (
        "id",
        "title",
    )


admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]
    list_display = (
        'id',
        'title',
    )
admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ["id", "product"]
    list_display = (
        'id',
        'product',
    )
admin.site.register(ProductImage, ProductImageAdmin)