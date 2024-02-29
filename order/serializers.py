# model
from .models import CodOrder, CodPurchaseProduct
from inventory.models import Size, ProductSizeVarient
# assets
# serializer
from product.serializers import ProductSerializer
from rest_framework import serializers


class CodPurchaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodPurchaseProduct
        fields = '__all__'
        extra_kwargs = {
            'order' : {'required': False},
            'product' : {'required': True},
            'quantity' : {'required': True},
        }
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['product']:
            data['product'] = ProductSerializer(instance.product, context= self.context).data
        return data

class CodOrderSerializer(serializers.ModelSerializer):
    purchase_order = CodPurchaseProductSerializer(many=True)
    class Meta:
        model = CodOrder
        fields = "__all__"
        extra_kwargs = {
            'billing_address' : {'required': True},
            'products' : {'required': False},
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
        purchase_order = validated_data.pop('purchase_order', [])

        validated_data['payment_status'] = 'UNPAID'
        validated_data['status'] = 'PENDING'
        

        order = super().create(validated_data)

        for i in purchase_order:
            _ordered =  CodPurchaseProduct.objects.create(order=order, **i)
            product_size_varient = _ordered.others_info.get('product_size_varient', None)
            if product_size_varient:
                size_title = product_size_varient.get('size_title', None)
                quantity = product_size_varient.get('quantity', 0)
                size = Size.objects.filter(size_title=size_title).first()
                product_varient = ProductSizeVarient.objects.filter(product=_ordered.product, size=size)
                print(quantity)
                if order.status == 'PENDING':
                    updated_quantity =  product_varient.first().quantity - quantity
                    product_varient.update(quantity=updated_quantity)
                elif order.status == 'CANCELLED':
                    updated_quantity =  product_varient.first().quantity + quantity
                    product_varient.update(quantity=updated_quantity)
        
        # 
        # sms_text = f"Your order has been confirmed.\n" + \
        #     f"Order ID:  {order.id}\n" + \
        #     f"Thank you for purchasing from www.krishijaat.com"

        # consumer_phn_number = instance.consumer.profile.phone_number
        # url = f'https://panel.smsbangladesh.com/api?user=krishijaatbd@gmail.com&password=bGZtgr3SWnvuHJU&from=KRISHIJAAT&to={consumer_phn_number}&text={sms_text}'
        # 
        
        return order
