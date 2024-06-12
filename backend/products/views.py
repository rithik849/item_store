from django.shortcuts import get_object_or_404, render
from rest_framework.fields import api_settings
from rest_framework.response import Response
from .serializers import ProductSerializer
from products.models import Product
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet): # type: ignore
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    pagination_class = PageNumberPagination
    
    # def list(self,request):
    #     queryset = Product.objects.all()
    #     serializer = ProductSerializer(queryset,many=True)
    #     # paginator = PageNumberPagination()
    #     # page = paginator.paginate_queryset(queryset=serializer.data, request=request)
    #     # if page is not None:
    #     #     return paginator.get_paginated_response(page) # type: ignore
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    # def retrieve(self, request, pk=None):
    #     queryset = Product.objects.all()
    #     product = get_object_or_404(queryset,pk = pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
    