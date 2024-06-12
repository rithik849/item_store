from rest_framework import routers
from django.urls import include, path

from item_store.views import ReviewViewSet, BasketViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register('review', ReviewViewSet, basename='review')
router.register('basket', BasketViewSet, basename='basket')
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('',include(router.urls))
]

