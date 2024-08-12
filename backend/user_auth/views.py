from typing import Optional
import typing
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from rest_framework import settings, status

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, GenericAPIView, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from collections import OrderedDict
from item_store.serializers import CustomerSerializer
from e_store.permissions import CustomerLogInViewPermission, IsNotAuthenticated
from item_store.models import Customer
from user_auth.serializers import SignUpSerializer, LogInSerializer, UpdateDetailsSerializer, UpdatePasswordSerializer
    
class CustomerSignUpView(CreateAPIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = SignUpSerializer
    
class CustomerChangeDetailsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateDetailsSerializer
    
    def get_object(self,pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404
    
    def post(self,request):
        # if type(request.user) == AnonymousUser:
        #     return Response({"success" : False, 'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        customer = request.user
        serializer = self.get_serializer(instance=customer,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            json = CustomerSerializer(serializer.instance)
            return Response({'success' : True, 'object': json.data, 'detail':'User data changed successfully'}, status=status.HTTP_200_OK)
        return Response({"success" : False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer
    
    def get_object(self,pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404
    
    def patch(self, request, pk=0):
        if type(request.user) == AnonymousUser:
            return Response({"success" : False, 'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        customer = request.user
        serializer = self.get_serializer(customer, data = request.data)
        if serializer.is_valid():
            serializer.save()
            json = CustomerSerializer(serializer.instance)
            return Response({'success' : True, 'object': json.data, 'detail': 'Password has been changed successfully.'}, status=status.HTTP_200_OK)
        return Response({"success" : False, 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
class CustomerLogInView(GenericAPIView):
    permission_classes = (CustomerLogInViewPermission,)
    serializer_class = LogInSerializer
    
    def get(self, request):
        if request.user.is_authenticated:
            json = CustomerSerializer(request.user)
            return Response({'is_authenticated' : True, 'customer' : json.data}, status=status.HTTP_200_OK)
        else:
            return Response({'is_authenticated' : False}, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            # if (not (type(data) is OrderedDict)) or (not ('email' in data)):
            #     raise Exception
            # user : Customer = Customer.objects.get(email=email)
            user : Optional[AbstractBaseUser] = authenticate(username=data['username'],password=data['password'])
            user = typing.cast(Customer,user)
            if user==None:
                raise Exception
            login(request, user)
            json = CustomerSerializer(user)
            return Response({
                "success" : True,
                "customer": json.data
                },status=status.HTTP_200_OK)
        except:
            return Response({'success' : False,'detail' : 'Username and Password not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomerLogOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogInSerializer
    
    def post(self,request):
        logout(request)

        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)