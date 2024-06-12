from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, Http404
from e_store.permissions import IsNotAuthenticated
from item_store.models import Customer
from token_auth.serializers import SignUpSerializer, LogInSerializer, UpdateDetailsSerializer, UpdatePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from collections import OrderedDict
from django.contrib.auth.models import AnonymousUser
    
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
            
            #user:Customer = authenticate(username=request.data['email'], password=request.data['password']) # type: ignore
            try:
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                
                if (not (type(data) is OrderedDict)) or (not ('email' in data)):
                    raise Exception
                email = data['email']
                user : Customer = Customer.objects.get(email=email)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success' : True,
                    'username': user.get_username(),
                    'email': user.email,
                    'token': token.key
                    },status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'success' : False, 'detail' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'success' : False,'detail' : 'Username and Password not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomerLogOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def delete(self,request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)