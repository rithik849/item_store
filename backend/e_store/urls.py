"""
URL configuration for e_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# class CustomerTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny ,)
#     serializer_class = CustomerTokenPairSerializer
    
#     def get(self,request):
#         return Response(data={"test":"here"})
    
# class CustomerTokenRefreshView(TokenRefreshView):
#     permission_classes = (IsAuthenticated ,)
#     authentication_classes = [JWTAuthentication]
#     serializer_class = CustomerTokenRefreshSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/token/',include('token_auth.urls')),
    path('admin/', admin.site.urls),
    path('product/',include("products.urls")),
    path('',include("item_store.urls"))
]

urlpatterns += [path('api-auth/',include('rest_framework.urls', namespace='rest_framework'))]
