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
from e_store.permissions import IsNotAuthenticated
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
            return Response({'success' : True, 'object': serializer.instance}, status=status.HTTP_200_OK)
        return Response({"success" : False, 'detail': 'Some details are invalid'}, status=status.HTTP_400_BAD_REQUEST)
    
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
            return Response({'success' : True, 'object': serializer.instance}, status=status.HTTP_200_OK)
        return Response({"success" : False, 'detail': 'Some details are invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class CustomerLogInView(GenericAPIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = LogInSerializer
    
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
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'success' : True,
                'username': user.get_username(),
                'email': user.email,
                'token': token.key
                },status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({'success' : False,'detail' : 'Username and Password not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomerLogOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogInSerializer
    
    def post(self,request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)

        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)