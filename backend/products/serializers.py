from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('url','name','price','type','stock')