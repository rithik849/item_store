from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
class DbCheckMiddleware(object):

    def process_request(self, request):
        try:
            "Some DB Code"
            success = True
        except:
            success = False                

        request.db_connection_successful = success
        
class ProductViewSet(viewsets.ViewSet):
    
    def list(self,request):
        pass
    
    def retrieve(self,request,pk=None):
        pass
    
    def update(self,request,pk=None):
        pass
    
    def create(self,request):
        pass
    