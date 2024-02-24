from django.contrib import admin
from .models import Size, ProductSizeVarient

# Register your models here.

class SizeAdmin(admin.ModelAdmin):
    search_fields = ["id", "size_title"]
    list_display = (
        "id",
        "size_title",
    )


admin.site.register(Size, SizeAdmin)


class ProductSizeVarientAdmin(admin.ModelAdmin):
    search_fields = ["id", "quantity"]
    list_display = (
        "id",
        "quantity",
    )
admin.site.register(ProductSizeVarient, ProductSizeVarientAdmin)