from rest_framework import routers
from rest_framework.routers import SimpleRouter, Route
from django.urls import include, path, re_path

from item_store.views import ReviewViewSet, BasketViewSet, OrderViewSet
from products.views import ProductViewSet

# class ReviewRouter(SimpleRouter):
#     routes = [
#         Route(
#             url=r'^{prefix}/$',
#             mapping={'get':'list'},
#             name = '{basename}-list',
#             detail=False,
#             initkwargs=None
#         ),
#         Route(
#             url=r'^{prefix}/{lookup}/$',
#             mapping={'get':'retrieve'},
#             name = '{basename}-retrieve',
#             detail=True,
#             initkwargs={'suffix' : 'Retrieve'}
#         )
#     ]

router = routers.DefaultRouter()
# router.register('review', ReviewViewSet, basename='review')
router.register('basket', BasketViewSet, basename='basket')
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('',include(router.urls)),
    path('review/<str:customer_username>/<int:product_id>/',
        ReviewViewSet.as_view({'get':'retrieve', 'delete':'destroy'}), name='review-detail'),
path('review/',
        ReviewViewSet.as_view({'get':'list','post':'create'}), name='review'),
]

