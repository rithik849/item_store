from django.contrib.auth.models import User, Group
from rest_framework import serializers
from item_store.models import Customer, Review, Basket, Order
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
        fields = ('username', 'email','password')
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
