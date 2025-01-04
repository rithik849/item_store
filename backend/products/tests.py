from django.contrib.auth.hashers import make_password
from django.test import TransactionTestCase, TestCase, Client
from rest_framework.test import APIClient, APIRequestFactory, api_settings, RequestsClient
from rest_framework.viewsets import reverse
from rest_framework import status

from item_store.models import Customer
from products.serializers import ProductSerializer
from products.models import Product
from products.views import ProductViewSet
from e_store.test_utils import my_reverse
import math

# Create your tests here.

class ProductTestCase(TransactionTestCase):
    fixtures = ['products.json']
    
    @classmethod
    def setUpClass(cls):
        cls.factory = APIRequestFactory()
        cls.user,val = Customer.objects.get_or_create(username='test',email='testuser@testuser.com')
        cls.user.set_password('testpassword123')
        
        
    
    def test_authenticated_users_are_allowed(self):
        client = APIClient()
        client.force_login(user=self.user)
        response=client.get('/products/')
        assert(response.status_code==200) # type: ignore
        assert(response.data['count']==3) # type: ignore
        response = client.get('/products/1/')
        assert(response.status_code==200) # type: ignore
        client.logout()
    
    def test_unauthenticated_users_are_allowed(self):
        client = APIClient()
        response=client.get('/products/')
        assert(response.status_code==200) # type: ignore
        assert(response.data['count']==3) # type: ignore
        response = client.get('/products/1/')
        assert(response.status_code==200) # type: ignore
    
    def test_retrieve_model(self):
        detail_view = ProductViewSet.as_view(actions={'get' : "retrieve"})
        product = Product.objects.get(id = 2)
        request = self.factory.get(reverse('product-detail',kwargs={'id' : product.id})) # type: ignore
        response = detail_view(request, id=2)
        
        serializer = ProductSerializer(product)
        
        assert(response.data==serializer.data)
        
    def test_list_model(self):
        PAGE_SIZE : int = api_settings.PAGE_SIZE # type: ignore
        list_view = ProductViewSet.as_view(actions = {'get' : 'list'})
        
        request = self.factory.get(reverse('product-list')) # type: ignore
        response = list_view(request)
        
        serializer = ProductSerializer(Product.objects.all(),many=True)
        pages = math.ceil(response.data['count'] / PAGE_SIZE)
        for i in range(1,pages+1):
            request = self.factory.get(my_reverse('product-list',query_kwargs={'page':i})) # type: ignore
            response = list_view(request)
            assert(response.data['results']==serializer.data[((i-1)*PAGE_SIZE) : ((i)*PAGE_SIZE)])