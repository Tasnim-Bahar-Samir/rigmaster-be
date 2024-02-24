# model
from .models import Product, Category, ProductImage
from inventory.models import ProductSizeVarient
# assets
# serializer
from inventory.serializers import ProductSizeVarientSerializer
from rest_framework import serializers

# category serializer 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            'title': {'required': True,"allow_null": False},
            'priority': {'required': False},
            'img': {'required': True, "allow_null": False},
        }



# product image serializer 
class ProductImageSrializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    _sl = serializers.IntegerField(required=False)
    class Meta:
        model = ProductImage
        fields = '__all__'

        extra_kwargs = {
            'product': {'required': False},       
            'image': {'required': True,"allow_null": False},       
        }

# product serial;izer
class ProductSerializer(serializers.ModelSerializer):
    product_size_varient = ProductSizeVarientSerializer(many=True, required = True)
    product_image = ProductImageSrializer(many=True, required = False)
    class Meta:
        model = Product
        fields = "__all__"

        extra_kwargs = {
            'title': {'required': True},
            'category': {'required': True},
            'meta_description': {'required': False},
            'description_html': {'required': False},
            'additional_information_html': {'required': False},
            'price': {'required': True},
        }

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['category']:
            print('in')
            data['category'] =  CategorySerializer(instance.category, context=self.context).data
        return data
    
    def create(self, validated_data):
        product_image = validated_data.pop("product_image", None)
        product_size_varient = validated_data.pop("product_size_varient", None)
        product = super().create(validated_data)
        if product_image:
            for i in product_image:
                ProductImage.objects.create(product=product, **i)
        if product_size_varient:
            for i in product_size_varient:
                ProductSizeVarient.objects.create(product=product, **i)

        
        return product
    
    def update(self, instance, validated_data):
        product_image = validated_data.pop("product_image", [])
        product_size_varient = validated_data.pop("product_size_varient", [])
        product = super().update(instance, validated_data)
        # if product_image:
        to_delete = list(ProductImage.objects.filter(product=instance).values_list("id", flat=True))
        for i in product_image:
            if "id" in i  and i["id"] in to_delete:
                to_delete.remove(i["id"])
            if i.get('id') and i.get('product') == product:
                ProductImage.objects.filter(id=i.get('id'), product=product).update(is_feature=i.get('is_feature'), _sl=i.get('_sl'))
            else: # add new image
                ProductImage.objects.create(product=product, **i)

        
        if len(product_image) == 0 :
            ProductImage.objects.filter(id__in = to_delete ,product=product).delete()
        else:
            ProductImage.objects.filter(id__in = to_delete ,product=product).delete()

        # product stock
        to_delete_product_stock = list(ProductSizeVarient.objects.filter(product=instance).values_list("id", flat=True))
        for i in product_size_varient:
            if "id" in i and i["id"] in to_delete_product_stock:
                to_delete_product_stock.remove(i["id"])
            if i.get('id') and i.get('product') == product:
                ProductSizeVarient.objects.filter(id=i.get('id'), product=product).update(unit=i.get('unit'), quantity=i.get('quantity'), price=i.get('price'))
            else :# add new stock)
                ProductSizeVarient.objects.create(product=product, **i)

        if len(product_size_varient) == 0 :
            ProductSizeVarient.objects.filter(id__in = to_delete_product_stock ,product=product).delete()
        else:
            ProductSizeVarient.objects.filter(id__in = to_delete_product_stock ,product=product).delete()
        

        return product