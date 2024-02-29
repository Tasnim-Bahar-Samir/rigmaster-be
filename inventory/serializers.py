from rest_framework import serializers

# model
from .models import Size, ProductSizeVarient


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

        extra_kwargs = {
            "size_title": {"required": True},
        }
    def validate(self, attrs):
        # print(self.)
        # if Supplier.objects.filter(phone_number=attrs.get('phone_number')).exists():
        #     raise serializers.ValidationError({"phone_number": 'This suplier is already exists'})

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

class ProductSizeVarientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductSizeVarient
        fields = "__all__"
        extra_kwargs = {
            "product": {"required": False},
            "size": {"required": True},
            "size_details": {"required": False}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        
        if data["size"]:
            data["size"] = SizeSerializer(instance.size).data

        if data["product"]:
            data['product'] =  {
                'id' : instance.product.id,
                'title' : instance.product.title
            }
        return data
