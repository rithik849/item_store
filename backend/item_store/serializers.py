from django.contrib.auth.models import User, Group
from rest_framework import serializers
from item_store.models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user : Customer):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username

        return token


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('url', 'name', 'email')
        

        
