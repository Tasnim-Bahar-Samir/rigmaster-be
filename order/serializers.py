from django.db.models import Sum
# model
from .models import CodOrder, CodPurchaseProduct, CusotmOrder, CustomPurchaseProduct
from inventory.models import Size, ProductSizeVarient

# assets
# serializer
from product.serializers import ProductSerializer,ProductSerializer2
from rest_framework import serializers


class CodPurchaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodPurchaseProduct
        fields = "__all__"
        extra_kwargs = {
            "order": {"required": False},
            "product": {"required": True},
            "quantity": {"required": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["product"]:
            data["product"] = ProductSerializer(
                instance.product, context=self.context
            ).data
        return data


class CodOrderSerializer(serializers.ModelSerializer):
    purchase_order = CodPurchaseProductSerializer(many=True)

    class Meta:
        model = CodOrder
        fields = "__all__"
        extra_kwargs = {
            "billing_address": {"required": True},
            "products": {"required": False},
        }

    def validate(self, attrs):
        purchase_order = attrs.get('purchase_order', None)
        if purchase_order:
            for order_item in purchase_order:
                product = order_item.get('product')
                quantity_requested = order_item.get('quantity')
                product_size_varient = order_item.get('others_info').get(
                "product_size_varient", None
                )
                size_title = product_size_varient.get('size_title')  # Assuming you have size information in purchase order
                size = Size.objects.filter(size_title=size_title).first()

                if not size:
                    raise serializers.ValidationError({'size': f"Size '{size_title}' not found"})

                product_variants = ProductSizeVarient.objects.filter(product=product, size=size)
                total_quantity = product_variants.aggregate(total=Sum('quantity'))['total']

                if total_quantity is None or quantity_requested > total_quantity:
                    raise serializers.ValidationError({'Insufficient Stock': f"{product.title} - {size_title}. Please update your cart."})

        return super().validate(attrs)


    def create(self, validated_data):
        purchase_order = validated_data.pop("purchase_order", [])

        validated_data["payment_status"] = "UNPAID"
        validated_data["status"] = "PENDING"

        order = super().create(validated_data)

        for i in purchase_order:
            purchaseProduct = CodPurchaseProduct.objects.create(order=order, **i)
            product_size_varient = purchaseProduct.others_info.get(
                "product_size_varient", None
            )
            if product_size_varient:
                size_title = product_size_varient.get("size_title", None)
                quantity = purchaseProduct.quantity
                size = Size.objects.filter(size_title=size_title).first()
                product_varient = ProductSizeVarient.objects.filter(
                    product=purchaseProduct.product, size=size
                )

                if order.status == "PENDING":
                    updated_quantity = product_varient.first().quantity - quantity
                    product_varient.update(quantity=updated_quantity)
                # elif order.status == 'CANCELLED':
                #     updated_quantity =  product_varient.first().quantity + quantity
                #     product_varient.update(quantity=updated_quantity)
        return order

    def update(self, instance, validated_data):
        order = super().update(instance, validated_data)
        purchaseProducts = CodPurchaseProduct.objects.filter(order=instance)
        for i in purchaseProducts:
            product_size_varient = i.others_info.get("product_size_varient", None)
            if product_size_varient:
                size_title = product_size_varient.get("size_title", None)
                quantity = i.quantity
                size = Size.objects.filter(size_title=size_title).first()
                product_varient = ProductSizeVarient.objects.filter(
                    product=i.product, size=size
                )

                if instance.status == "CANCELLED":
                    updated_quantity = product_varient.first().quantity + quantity
                    product_varient.update(quantity=updated_quantity)

        return order
    
class  CustomPurchaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPurchaseProduct
        fields = "__all__"
        extra_kwargs = {
            "order": {"required": False},
            "product": {"required": True},
            "quantity": {"required": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["product"]:
            data["product"] = ProductSerializer2(
                instance.product, context=self.context
            ).data
        return data


class CustomOrderSerializer(serializers.ModelSerializer):
    custom_purchase_order = CustomPurchaseProductSerializer(many=True)

    class Meta:
        model = CusotmOrder
        fields = "__all__"
        extra_kwargs = {
            "billing_address": {"required": True},
            "products": {"required": False},
        }

    def validate(self, attrs):
        # purchase_order = attrs.get('purchase_order', None)
        # if purchase_order:
        #     for i in purchase_order:
        #         product = i.get('product')
        #         total_quantity = Inventatory.objects.filter(inventory_product=product).aggregate(total_sum=Sum('inward_quantity'))['total_sum']

        #         if not total_quantity or i.get('quantity') >= total_quantity:
        #             raise serializers.ValidationError({'stock_out': f"{product.title} stock out"})
        return super().validate(attrs)

    def create(self, validated_data):
        purchase_order = validated_data.pop("custom_purchase_order", [])

        validated_data["payment_status"] = "UNPAID"
        validated_data["status"] = "PENDING"

        order = super().create(validated_data)

        for i in purchase_order:
            purchaseProduct = CustomPurchaseProduct.objects.create(order=order, **i)
            product_size_varient = purchaseProduct.others_info.get(
                "product_size_varient", None
            )
            if product_size_varient:
                size_title = product_size_varient.get("size_title", None)
                quantity = purchaseProduct.quantity
                size = Size.objects.filter(size_title=size_title).first()
                product_varient = ProductSizeVarient.objects.filter(
                    product=purchaseProduct.product, size=size
                )

                if order.status == "PENDING":
                    updated_quantity = product_varient.first().quantity - quantity
                    product_varient.update(quantity=updated_quantity)
                # elif order.status == 'CANCELLED':
                #     updated_quantity =  product_varient.first().quantity + quantity
                #     product_varient.update(quantity=updated_quantity)
        return order

    def update(self, instance, validated_data):
        order = super().update(instance, validated_data)
        purchaseProducts = CustomPurchaseProduct.objects.filter(order=instance)
        for i in purchaseProducts:
            product_size_varient = i.others_info.get("product_size_varient", None)
            if product_size_varient:
                size_title = product_size_varient.get("size_title", None)
                quantity = i.quantity
                size = Size.objects.filter(size_title=size_title).first()
                product_varient = ProductSizeVarient.objects.filter(
                    product=i.product, size=size
                )

                if instance.status == "CANCELLED":
                    updated_quantity = product_varient.first().quantity + quantity
                    product_varient.update(quantity=updated_quantity)

        return order
