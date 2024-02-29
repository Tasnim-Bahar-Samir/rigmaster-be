from django.db import models

# model
from django.contrib.auth.models import User
from product.models import Product
import uuid

# options
PAYMENT_STATUS = [
    ('UNPAID', 'Unpaid'),
    ('PAID', 'Paid'),
    ('PERCIAL_PAID', 'Partial Paid'),
]
ORDER_STATUS = [
    ('PENDING', 'Pending'),
    ('PROCESS', 'Process'),
    ('SHIFT', 'Shift'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
]

# Create your models here.


class CodOrder(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    payment_status = models.CharField(max_length=20, default="UNPAID", choices=PAYMENT_STATUS)
    status = models.CharField(max_length=20, default="PENDING", choices=ORDER_STATUS)
    billing_address = models.JSONField(null=True, blank=True)
    shipping_address = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CodPurchaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    order = models.ForeignKey(CodOrder, null=True , related_name='purchase_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True , related_name='purchase_order_product', on_delete=models.SET_NULL)
    quantity = models.FloatField(null=True)
    others_info = models.JSONField(null=True, blank=True)