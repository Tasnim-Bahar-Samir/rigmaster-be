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
    order_id = models.CharField(max_length=100, unique=True, null=True, editable=False)
    payment_status = models.CharField(max_length=20, default="UNPAID", choices=PAYMENT_STATUS)
    status = models.CharField(max_length=20, default="PENDING", choices=ORDER_STATUS)
    billing_address = models.JSONField(null=True, blank=True)
    shipping_address = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = CodOrder.objects.order_by('-id').first()
            last_order_id = int(last_order.order_id.split('-')[1]) if last_order else 0
            new_order_id = f"RM-{last_order_id + 1:06d}"
            
            # Check if the generated order_id already exists, if so, generate a new one
            while CodOrder.objects.filter(order_id=new_order_id).exists():
                last_order_id += 1
                new_order_id = f"RM-{last_order_id + 1:06d}"
            
            self.order_id = new_order_id

        super(CodOrder, self).save(*args, **kwargs)

class CodPurchaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    order = models.ForeignKey(CodOrder, null=True , related_name='purchase_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True , related_name='purchase_order_product', on_delete=models.SET_NULL)
    quantity = models.FloatField(null=True)
    others_info = models.JSONField(null=True, blank=True)
    
    
class CusotmOrder(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    order_id = models.CharField(max_length=100, unique=True, null=True, editable=False)
    payment_status = models.CharField(max_length=20, default="UNPAID", choices=PAYMENT_STATUS)
    status = models.CharField(max_length=20, default="PENDING", choices=ORDER_STATUS)
    billing_address = models.JSONField(null=True, blank=True)
    shipping_address = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = CusotmOrder.objects.order_by('-id').first()
            last_order_id = int(last_order.order_id.split('-')[1]) if last_order else 0
            new_order_id = f"RM-{last_order_id + 1:06d}"
            
            # Check if the generated order_id already exists, if so, generate a new one
            while CusotmOrder.objects.filter(order_id=new_order_id).exists():
                last_order_id += 1
                new_order_id = f"RM-{last_order_id + 1:06d}"
            
            self.order_id = new_order_id

        super(CusotmOrder, self).save(*args, **kwargs)

class CustomPurchaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    order = models.ForeignKey(CusotmOrder, null=True , related_name='custom_purchase_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True , related_name='custom_purchase_order_product', on_delete=models.SET_NULL)
    quantity = models.FloatField(null=True)
    others_info = models.JSONField(null=True, blank=True)