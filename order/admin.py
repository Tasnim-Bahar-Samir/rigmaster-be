from django.contrib import admin
from .models import CodOrder, CodPurchaseProduct, CusotmOrder,CustomPurchaseProduct

# Register your models here.


class CodOrderAdmin(admin.ModelAdmin):
    search_fields = ["id", "payment_status","status"]
    list_display = (
        'id',
        'order_id',
        'payment_status',
        'status',
    )
admin.site.register(CodOrder, CodOrderAdmin)

class CodPurchaseProductAdmin(admin.ModelAdmin):
    search_fields = ["id", "payment_status","status"]
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
    )
admin.site.register(CodPurchaseProduct, CodPurchaseProductAdmin)

class CustomOrderAdmin(admin.ModelAdmin):
    search_fields = ["id", "payment_status","status"]
    list_display = (
        'id',
        'order_id',
        'payment_status',
        'status',
    )
admin.site.register(CusotmOrder, CustomOrderAdmin)

class CustomhaseProductAdmin(admin.ModelAdmin):
    search_fields = ["id", "payment_status","status"]
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
    )
admin.site.register(CustomPurchaseProduct, CustomhaseProductAdmin)
