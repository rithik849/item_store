from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models.manager import BaseManager
from rest_framework import viewsets
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from e_store.permissions import ReviewPermission
from products.models import Product
from item_store.models import Order, OrderNumber, Review, Basket, Customer
from item_store.serializers import CreateOrderSerializer, OrderNumberSerializer, OrderSerializer, RemoveFromBasketSerializer, ReviewSerializer, BasketSerializer, AddToBasketSerializer
from products.views import GetUserMixin

def paginate(request,data,paginator):
        page = paginator.paginate_queryset(queryset=data, request=request)
        if page is not None:
            return paginator.get_paginated_response(page) # type: ignore
        return Response(data,status=status.HTTP_200_OK)

# Review: Customers should be able to view and post reviews of products.
class ReviewViewSet(
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin):
    
    permission_classes = [ReviewPermission]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def create(self, request):
        user = request.user
        serializer = ReviewSerializer(customer=user.id, 
                                      product=request.data['product_id'], 
                                      rating=request.data['rating'], 
                                      comment=request.data['comment'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def destroy(self,request):
        user = request.user
        review : Review = get_object_or_404(klass=Review,customer=user.id,product=request.data['product_id'])
        review.delete()
        return Response("Your review has been successfully deleted", status=status.HTTP_200_OK)

# Basket: Customers should be able to view their basket, add items to their basket and remove items from their basket.
class BasketViewSet(
    viewsets.GenericViewSet,
    GetUserMixin):
    
    def retrieve(self, request, pk=None):
        customer = self.get_object()
        items = Basket.objects.filter(customer = customer.id)
        serializer = BasketSerializer(items,many=True)
        
        return paginate(request,serializer.data,self.paginator)
    
    def create(self, request, *args, **kwargs):
        serializer_class = AddToBasketSerializer
        # Get the authenticated users basket and search if the product exists in the basket
        user: Customer = self.get_object() # type: ignore
        baskets: BaseManager[Basket]= Basket.objects.filter(customer = request.user.id)
        entry_for_product = baskets.filter(product_id=request.data['product_id'])
        
        if entry_for_product.count() == 0:
            serializer = serializer_class(data={'customer' : user.id, 'product' : request.data['product_id'], 'quantity' : request.data['quantity']}) # type: ignore
        else:
            serializer = serializer_class(instance = entry_for_product[0], data = {'quantity' : request.data['quantity']}, partial = True)
        
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"success" : True,"detail" : "Product added to basket"},status=status.HTTP_200_OK)

    def destroy(self,request):
        user: Customer = self.get_object() # type: ignore
        basket: BaseManager[Basket]= Basket.objects.filter(customer = user.id)  # type: ignore
        entry_for_product = basket.get(product_id=request.data['product_id'])
        
        serializer = RemoveFromBasketSerializer(instance = entry_for_product, data = {'quantity' : request.data['quantity']}, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"success" : True,"detail" : "Product decremented from basket"},status=status.HTTP_200_OK)
    
# Order: Customers should be able to view their previous orders.
class OrderViewSet(viewsets.GenericViewSet,
                   GetUserMixin):

    # List orders made by a customer
    def list(self, request):
        customer: Customer = self.get_object()
        orders : BaseManager[OrderNumber] = OrderNumber.objects.filter(customer=customer.id).order_by("-date") # type:ignore
        serializer = OrderNumberSerializer(orders,many=True)
        
        return paginate(request,serializer.data,self.paginator)
    
    # Retrieve the products part of the order
    def retrieve(self, request):
        customer: Customer = self.get_object()
        order_number : OrderNumber = OrderNumber.objects.get(customer=customer.id,id = request.data['order_id']) # type:ignore
        items : BaseManager[Order] = Order.objects.filter(order_number=order_number.id) # type: ignore
        serializer = OrderSerializer(items,many=True)
        
        return paginate(request,serializer.data,self.paginator)
    
    def create(self, request):
        """
        Create an order by taking the customer and items in their basket
        and create an orderNum entry. For each item we create an entry in Order using orderNum,
        decrementing items from Product.
        """
        user : Customer = self.get_object()
        items = Basket.objects.filter(customer=user.id) # type: ignore
        
        # Need to validate against products incase quantities have changed
        serializer = BasketSerializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        # Reduce the stock of each product
        for item in data:
            id = item['product']
            product = Product.objects.get(id=id)
            product.stock -= item['quantity']
            product.save()
        # Remove items from the basket
        items.delete()

        # Create the order
        order_ref = OrderNumber(customer=user.id) #type: ignore
        order_ref.save()
        serializer = CreateOrderSerializer(data=data, 
                                        context = {'order_id' : order_ref.id}, # type: ignore
                                        many=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"success" : True, "detail" : "Order has been made"},status=status.HTTP_200_OK)