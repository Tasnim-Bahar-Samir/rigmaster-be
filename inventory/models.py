# model
from django.db import models
from product.models import Product

# utils


class Size(models.Model):
    size_title = models.CharField(max_length=20, null=True)
    size_details = models.CharField(max_length=500, null=True)
    shirt_size_details = models.CharField(max_length=500, null=True)
    polo_size_details = models.CharField(max_length=500, null=True)
    def __str__(self):
        return self.size_title
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ProductSizeVarient(models.Model):
    product = models.ForeignKey(Product, related_name="product_size_varient", blank=True, null=True, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name="product_stock_size", blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0, null=True)
