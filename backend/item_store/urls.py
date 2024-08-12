from rest_framework import routers
from rest_framework.routers import DefaultRouter, Route
from django.urls import include, path, re_path

from item_store.views import ReviewViewSet, BasketViewSet, OrderViewSet
from products.views import ProductViewSet

class ReviewRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get':'list', 'post':'create'},
            name = '{basename}-list',
            detail=False,
            initkwargs={'suffix' : "List"}
        ),
        Route(
            url=r'^{prefix}/(?P<product_id>[0-9]+)/$',
            mapping={'get':'get_reviews_for_product'},
            name = '{basename}-list',
            detail=True,
            initkwargs={'suffix' : "List"}
        ),
        Route(
            url=r'^{prefix}/(?P<customer_username>[-a-zA-Z0-9_]+)/(?P<product_id>[0-9]+)/$',
            mapping={'get':'retrieve','delete':'destroy'},
            name = '{basename}-detail',
            detail=True,
            initkwargs={'suffix' : 'Instance'}
        )
    ]
    
class OrderRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get':'list', 'post':'create'},
            name = '{basename}-list',
            detail=False,
            initkwargs={'suffix' : "List"}
        ),
        Route(
            url=r"^{prefix}/(?P<date>\d\d\d\d-\d\d-\d\d)/(?P<id>[0-9]+)/$",
            mapping={'get':'retrieve'},
            name = '{basename}-detail',
            detail=True,
            initkwargs={'suffix' : 'Instance'}
        )
    ]

router = routers.SimpleRouter()
router.register('baskets', BasketViewSet, basename='basket')
order_router = OrderRouter()
order_router.register('orders',OrderViewSet, basename='order')

review_router = ReviewRouter()
review_router.register('reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('',include(review_router.urls)),
    path('',include(router.urls)),
    path('',include(order_router.urls))
]

