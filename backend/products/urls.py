from django.urls import include, path
from rest_framework import routers

from products import views

router = routers.DefaultRouter()
router.register('', views.ProductViewSet,basename='product')
urlpatterns = [
    path('',include(router.urls))
]
