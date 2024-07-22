from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from products.serializers import ProductSerializer
from item_store.models import Customer, OrderNumber, Review, Basket, Order, Product

from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from rest_framework.reverse import reverse

class ParameterisedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    Represents the instance, or a property on the instance, using hyperlinking.

    lookup_fields is a tuple of tuples of the form:
        ('model_field', 'url_parameter')
    """
    lookup_fields = (('pk', 'pk'),)

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        super(ParameterisedHyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            attr = obj
            model_field = model_field[1:-1]
            # print(model_field)
            for field in model_field.split('_'):
                # print(field)
                attr = getattr(attr,field)#getattr(attr,field)
            kwargs[url_param] = attr
        # print(kwargs)

        return reverse(view_name, kwargs=kwargs, request=request, format=format)


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
        

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name="review-detail", lookup_fields=(('<customer_username>', 'customer_username'), ('<product_id>', 'product_id')), read_only=True)
    customer = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = Review
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'url': {'lookup_fields' : ['customer_username','product_id']}
            }


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
class BasketSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Basket
        depth=1
        fields = '__all__'
        
    # Validate that quantity is less than  or equal to what is in stock
    def validate(self, data):
        print("HERE " + str(data))
        product = Product.objects.get(id = data['product'])
        if product.stock < data['quantity']:
            raise serializers.ValidationError("Not enough of product " +str(product.name)+ " in stock")
        return data
    
    def create(self,validated_data):
        entry = Basket(**validated_data)
        entry.save()
        return entry

class BasketHyperLinkedIdentityField(serializers.HyperlinkedIdentityField):
    view_name = 'basket-detail'
    
    def get_url(self,obj,view_name,request,format):
        url_kwargs = {
            "id" : obj.product.id
        }
        return reverse(view_name, kwargs = url_kwargs, request = request, format = format)
        
        
class BasketListViewSerializer(serializers.ModelSerializer):
    url = BasketHyperLinkedIdentityField(view_name='basket-detail', read_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', lookup_field='id', read_only=True)
    
    class Meta:
        model = Basket
        depth=1
        fields = '__all__'
        extra_kwargs = {
            'url' : {'lookup_field' : 'id' }
        }


class OrderBasketSerializer(BasketSerializer):
    class Meta:
        model = Basket
        fields = "__all__"
        
        
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
        
class RemoveFromBasketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Basket
        fields = '__all__'
        
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
            return instance
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = '__all__'


class OrderNumberSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='order-detail', lookup_fields=(("<date>","date"),("<id>","id")))
    items = serializers.SerializerMethodField() 
    customer = CustomerSerializer()
    
    class Meta:
        model = OrderNumber
        fields = '__all__'
        
    def get_items(self,obj):
        orders = Order.objects.filter(order_number = obj.id)
        serializers = OrderSerializer(orders, many=True)
        return serializers.data
    
    
class CreateOrderSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    
    # class Meta:
    #     model = Basket
    #     fields = ('product_id','quantity')
    
    def create(self,validated_data):
        # Need to have order num to create order
        order_id = self.context['order_id']
        print("HERE")
        print(validated_data)
        order = Order(order_number = order_id,
                product = validated_data['product_id'],
                quantity = validated_data['quantity'])
        order.save()
