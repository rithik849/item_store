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
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from django.urls import path, include
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token

from e_store.permissions import IsNotAuthenticated
    

# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
    path('customers/',include('user_auth.urls')),
    path('admin/', admin.site.urls),
    path('products/',include("products.urls")),
    path('',include("item_store.urls"))
]

urlpatterns += [path('api-auth/',include('rest_framework.urls', namespace='rest_framework'))
                ]
