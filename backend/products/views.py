from rest_framework import viewsets
from products.serializers import ProductSerializer
from products.models import Product
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

# Create your views here.
class ProductViewSet(RetrieveModelMixin,ListModelMixin,viewsets.GenericViewSet): # type: ignore
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    
    