from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from products.serializers import ProductSerializer
from item_store.models import Customer, OrderNumber, Review, Basket, Order, Product

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user : Customer):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username

        return token


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'email')
        

class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = Review
        fields = '__all__'
        depth = 1
        
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
class BasketSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Basket
        depth=1
        # fields = '__all__'
        exclude = ['customer']
        extra_kwargs = {
            "url" : {"lookup_field" : "id"}
        }
        
    # Validate that quantity is less than  or equal to what is in stock
    def validate(self, data):
        product = Product.objects.get(id = data['product'])
        if product.stock < data['quantity']:
            raise serializers.ValidationError("Not enough of product " +str(product.name)+ " in stock")
        return data
    
    def create(self,validated_data):
        entry = Basket(**validated_data)
        entry.save()
        return entry
    

class AddToBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Basket
        fields = '__all__'
    # Validate that quantity is less than  or equal to what is in stock
    def validate(self, data):
        basket = self.instance
        if basket:
            product = basket.product
            initial_quantity = basket.quantity
        else:
            product = data['product']
            initial_quantity = 0
        if product.stock < initial_quantity + data['quantity']:
            raise serializers.ValidationError("Not enough of product " +str(product.name)+ " in stock")
        return data
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            if attr!='quantity':
                instance[attr] = value
        if 'quantity' in validated_data:
            instance.quantity += validated_data['quantity'] 
        instance.save()
        return instance
        
class RemoveFromBasketSerializer(BasketSerializer):
    # Validate that quantity is less than  or equal to what is in stock
    def validate(self, data):
        basket : Basket = self.instance # type: ignore
        initial_quantity = basket.quantity
        if ((initial_quantity - data['quantity']) < 0):
            raise serializers.ValidationError("Basket quantity is less than the quantity to remove.")
        return data
    
    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            instance.quantity -= validated_data['quantity']
        # Remove if we have no items in the basket
        if instance.quantity==0:
            instance.delete()
            return None
        instance.save()
        return instance
    
class OrderNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderNumber
        fields = '__all__'
    
class CreateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self,validated_data):
        # Need to have order num to create order
        order_id = self.context['order_id']
        
        for item in validated_data:
            order = Order(order_number = order_id,
                  product = item.product,
                  quantity = item.quantity)
            order.save()
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
