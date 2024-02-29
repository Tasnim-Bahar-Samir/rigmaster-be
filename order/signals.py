# # model
# from .models import CodOrder, CodPurchaseProduct
# from inventory.models import Size, ProductSizeVarient
# # assets
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# @receiver(pre_save, sender=CodOrder)
# def manage_inventory(sender, instance, *args, **kwargs):
#     purchase = CodPurchaseProduct.objects.filter(order=instance)
#     for i in purchase:
#         product_size_varient = i.others_info.get('product_size_varient', None)
#         if product_size_varient:
#             size_title = product_size_varient.get('size_title', None)
#             quantity = product_size_varient.get('quantity', 0)
#             size = Size.objects.filter(size_title=size_title).first()
#             product_varient = ProductSizeVarient.objects.filter(product=i.product, size=size)
#             if instance.status == 'PENDING':
#                 updated_quantity =  product_varient.first().quantity - quantity
#                 product_varient.update(quantity=updated_quantity)
#             elif instance.status == 'CANCELLED':
#                 updated_quantity =  product_varient.first().quantity + quantity
#                 product_varient.update(quantity=updated_quantity)
