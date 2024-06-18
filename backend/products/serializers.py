from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','price','type','stock')
        
class UpdateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
        
    # Negative quantity, we remove product, positive we add product
    def validate(self,data):
        if self.instance.stock + data['quantity'] < 0: # type: ignore
            raise Exception("Not enough of product "+str(self.instance)+" in stock")
        return data
    
    def update(self,instance,validated_data):
        instance.stock += validated_data['quantity']
        instance.save()
        return instance