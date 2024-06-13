from django.shortcuts import get_object_or_404, render
from rest_framework.fields import api_settings
from rest_framework.response import Response
from .serializers import ProductSerializer
from products.models import Product
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

class GetUserMixin:
    
    def get_object(self):
        return self.request.user # type: ignore

# Create your views here.
class ProductViewSet(RetrieveModelMixin,ListModelMixin,viewsets.GenericViewSet): # type: ignore
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    pagination_class = PageNumberPagination
    
    