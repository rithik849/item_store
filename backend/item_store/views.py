from django.shortcuts import get_object_or_404
from django.db.models.manager import BaseManager
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import csrf_exempt
from rest_framework.decorators import action
from e_store.permissions import IsCustomerPermission, IsOwnerPermission, ReviewPermission
from products.models import Product
from products.serializers import UpdateProductSerializer
from item_store.models import Order, OrderNumber, Review, Basket, Customer
from item_store.serializers import BasketListViewSerializer, CreateOrderSerializer, CustomerSerializer, OrderBasketSerializer, OrderNumberSerializer, OrderSerializer, RemoveFromBasketSerializer, CreateReviewSerializer,ReviewSerializer, BasketSerializer, AddToBasketSerializer
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token
from django.utils.decorators import method_decorator

def paginate(request,data,paginator):
        page = paginator.paginate_queryset(queryset=data, request=request)
        if page is not None:
            return paginator.get_paginated_response(page) # type: ignore
        return Response(data,status=status.HTTP_200_OK)
    
# Review: Customers should be able to view and post reviews of products.
# @method_decorator(csrf_exempt,name='list')
class ReviewViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet):
    
    permission_classes = [ReviewPermission]
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    lookup_fields = ['customer_username','product_id']
    
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
            
        user = Customer.objects.get(username=filter['customer_username'])
        del filter['customer_username']
        filter['customer'] = user
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
        
    def create(self, request):
        user = request.user
        request.data['customer'] = user.id
        serializer = CreateReviewSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def destroy(self,request, customer_username=None, product_id=None):
        user = request.user
        review : Review = self.get_object()
        review.delete()
        return Response("Your review has been successfully deleted", status=status.HTTP_200_OK)

# Basket: Customers should be able to view their basket, add items to their basket and remove items from their basket.
# @method_decorator(csrf_protect,name='dispatch')
class BasketViewSet(
    viewsets.GenericViewSet
    ):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_field = 'id'
    permission_classes = [IsOwnerPermission]
    
    def get_queryset(self):
        return Basket.objects.filter(customer=self.request.user) # type: ignore
    
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        filter["product__id"] = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset,**filter)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def retrieve(self,request,id=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def list(self, request):
        customer = self.request.user
        items = self.get_queryset()# Basket.objects.filter(customer = customer.id) # type: ignore
        serializer = BasketListViewSerializer(items,many=True,context = {"request":request})
        
        return paginate(request,serializer.data,self.paginator)
    
    def create(self, request, *args,**kwargs):
        serializer_class = AddToBasketSerializer
        # Get the authenticated users basket and search if the product exists in the basket
        user: Customer = self.request.user # type: ignore
        baskets: BaseManager[Basket]= self.get_queryset()
        entry_for_product = baskets.filter(product_id=request.data['product'])
        if request.data['quantity'] <= 0:
            raise APIException("Can only have a positive quantity of a product")
        if entry_for_product.count() == 0:
            serializer = serializer_class(data={'customer' : user.id, 'product' : request.data['product'], 'quantity' : request.data['quantity']}) # type: ignore
        else:
            serializer = serializer_class(instance = entry_for_product[0], data = {'quantity' : request.data['quantity']}, partial = True)
        
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"success" : True,"detail" : "Product "+str(entry_for_product[0].product)+" added to basket"},status=status.HTTP_200_OK)
    
    def delete(self, request, id=None):
        if id==None:
            items = self.get_queryset()
            items.delete()
            return Response({"success":True, "detail": "All items removed from basket"}, status=status.HTTP_200_OK)
        user : Customer = request.user
        item : Basket = self.get_object()
        item.delete()
        return Response({"success":True, "detail": "Item removed from basket"}, status=status.HTTP_200_OK)
        
    def partial_update(self, request, id = None):
        user: Customer = self.request.user # type: ignore
        basket: BaseManager[Basket]= self.get_queryset()
        entry_for_product = self.get_object()
        quantity = request.data['quantity']
        # We either increase quantity in basket or decrease quantity in basket. Product quantity gets updated at order
        if quantity < 0:
            serializer = RemoveFromBasketSerializer(instance = entry_for_product, data = {'quantity' : -quantity}, partial = True)
        else:
            serializer = AddToBasketSerializer(instance = entry_for_product, data = {'quantity' : quantity}, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        change = "unchanged"
        if quantity < 0:
            change = "decreased"
        elif quantity > 0:
            change = "increased"
            
        return Response({"success" : True,"detail" : "Product "+str(entry_for_product.product)+f" quantity {change}"},status=status.HTTP_200_OK)
    
# Order: Customers should be able to view their previous orders.
class OrderViewSet(
    viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'
    
    def get_queryset(self):
        return OrderNumber.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        serializers = {
            'list' : OrderNumberSerializer,
            'retrieve' : OrderNumberSerializer,
            'create' : CreateOrderSerializer,
        }
        return serializers[self.action]
        

    # List orders made by a customer
    def list(self, request):
        customer: Customer = self.request.user # type: ignore
        orders : BaseManager[OrderNumber] = OrderNumber.objects.filter(customer=customer).order_by("-date") # type:ignore
        serializer = self.get_serializer_class()
        serializer = serializer(orders, many=True, context = {'request' : request})
        
        return paginate(request,serializer.data,self.paginator)
    
    # Retrieve the products part of the order
    def retrieve(self,request, date=None, id=None):
        customer: Customer = self.request.user # type: ignore
        order_number : OrderNumber = OrderNumber.objects.get(customer=customer.id,date=date, id=id) # type:ignore
        # items : BaseManager[Order] = Order.objects.filter(order_number=order_number.id) # type: ignore
        serializer = self.get_serializer_class()
        serializer = serializer(order_number,context = {'request' : request})
        
        return paginate(request,serializer.data['items'],self.paginator)
    
    def create(self, request):
        """
        Create an order by taking the customer and items in their basket
        and create an orderNum entry. For each item we create an entry in Order using orderNum,
        decrementing items from Product.
        """
        user : Customer = self.request.user # type: ignore
        items = Basket.objects.filter(customer=user) # type: ignore
        print('here '+str(items))
        
        if items.count()==0:
            raise APIException("You do not have items in your basket.")
        
        print('here2')
        
        # Need to validate against products incase quantities have changed
        
        for item in items:
            if item.product.stock < item.quantity:
                raise APIException("Not enough of "+str(item.product)+" in stock")
            
        
        print('here3')
        
        
        # Reduce the stock of each product
        for item in items:
            print(item)
            product = item.product
            product_serializer = UpdateProductSerializer(instance=product, data = {"stock" : -item.quantity},partial=True)
            product_serializer.is_valid(raise_exception=True)
            print('here4')
            product_serializer.save()
        
        print('here4')

        # Create the order
        order_ref = OrderNumber(customer=user) #type: ignore
        order_ref.save()
        print(list(items.values()))
        serializer = self.get_serializer_class()
        serializer = serializer(data=list(items.values()), 
                                        context = {'order_id' : order_ref}, # type: ignore
                                        many=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Remove items from the basket
        items.delete()
        print("here5")
        
        return Response({"success" : True, "detail" : "Order has been made"},status=status.HTTP_200_OK)