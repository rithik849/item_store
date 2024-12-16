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
        fields = ('username', 'email','total_basket_cost')
        

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
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('customer', 'product'),
                message="Customer already has a review for this product."
            )
        ]
        
    def validate(self,data):
        has_review = Review.objects.filter(customer=data['customer'], product=data['product']).exists()
        if has_review:
            raise serializers.ValidationError("Customer already has a review for this product")
        return data
    
class BasketSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Basket
        depth=1
        fields = '__all__'
        
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

class BasketHyperLinkedIdentityField(serializers.HyperlinkedIdentityField):
    view_name = 'basket-detail'
    
    def get_url(self,obj,view_name,request,format):
        url_kwargs = {
            "id" : obj.product.id
        }
        return reverse(view_name, kwargs = url_kwargs, request = request, format = format)
        
        
class BasketListViewSerializer(serializers.ModelSerializer):
    url = BasketHyperLinkedIdentityField(view_name = 'basket-detail', read_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset = Customer.objects.all())
    
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
        
        
class ChangeBasketQuantitySerializer(serializers.ModelSerializer):
    
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
        if data['quantity'] < 0:
            raise serializers.ValidationError("Can not have a negative quantity of an item.")
        # if product.stock < initial_quantity + data['quantity']:
        if product.stock < data['quantity']:
            raise serializers.ValidationError("Not enough of product " +str(product.name)+ " in stock")
        return data
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            if attr!='quantity':
                instance[attr] = value
        if 'quantity' in validated_data:
            # instance.quantity += validated_data['quantity'] 
            instance.quantity = validated_data['quantity']
        if (instance.quantity==0):
            instance.delete()
        else:
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

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(OrderNumberSerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)
        
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
        order = Order(order_number = order_id,
                product = validated_data['product_id'],
                quantity = validated_data['quantity'])
        order.save()
