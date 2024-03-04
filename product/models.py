from django.db import models
from ckeditor.fields import RichTextField

# utils
from django_resized import ResizedImageField
from autoslug import AutoSlugField
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    priority = models.FloatField(default=0, null=True)
    title = models.CharField(max_length=150, null=True, unique=True)
    slug = AutoSlugField(populate_from='title', null=True, blank=True, always_update=True)
    img = ResizedImageField(
        null=True,
        blank=True,
        upload_to="Product/category/img",
        max_length=5000,
        force_format="WEBP",
        quality=75,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    priority = models.FloatField(default=0, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name="category",
        on_delete=models.SET_NULL,
    )
    meta_description = models.CharField(max_length=250, blank=True, null=True)
    description_html = RichTextField(blank=True, null=True)
    additional_information_html = RichTextField(blank=True, null=True)
    # selling_price = models.FloatField(null=True)
    price = models.FloatField(null=True)
    color= models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    _sl = models.IntegerField(default=0, null=True)
    product = models.ForeignKey(
        Product, related_name="product_image", null=True, on_delete=models.CASCADE
    )
    image = ResizedImageField(
        null=True,
        blank=True,
        upload_to="Product/productImage/image",
        max_length=5000,
        force_format="WEBP",
        quality=75,
    )
    is_feature = models.BooleanField(default=False, null=True)
