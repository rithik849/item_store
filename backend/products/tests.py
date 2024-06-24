from django.test import TransactionTestCase, TestCase, Client
from rest_framework.test import APIClient, APIRequestFactory, api_settings
from rest_framework.viewsets import reverse

from products.serializers import ProductSerializer
from products.models import Product
from products.views import ProductViewSet

# Create your tests here.

from django.utils.http import urlencode

def my_reverse(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return f'{url}?{urlencode(query_kwargs)}'

    return url

class ProductTestCase(TransactionTestCase):
    fixtures = ['products.json']
    
    def setUp(self):
        self.factory = APIRequestFactory()
        
    
    def test_retrieve_model(self):
        detail_view = ProductViewSet.as_view(actions={'get' : "retrieve"})
        product = Product.objects.get(id = 2)
        request = self.factory.get(reverse('product-detail',kwargs={'id' : product.id})) # type: ignore
        response = detail_view(request,id=2)
        
        serializer = ProductSerializer(product)
        
        assert(response.data==serializer.data)
        
    def test_list_model(self):
        PAGE_SIZE : int = api_settings.PAGE_SIZE # type: ignore
        list_view = ProductViewSet.as_view(actions = {'get' : 'list'})
        
        request = self.factory.get(reverse('product-list')) # type: ignore
        response = list_view(request)
        
        serializer = ProductSerializer(Product.objects.all(),many=True)
        pages = response.data['count']
        for i in range(1,pages):
            request = self.factory.get(my_reverse('product-list',query_kwargs={'page':i})) # type: ignore
            response = list_view(request)
            assert(response.data['results']==serializer.data[((i-1)*PAGE_SIZE) : ((i)*PAGE_SIZE)])