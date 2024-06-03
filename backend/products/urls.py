from django.urls import include, path
from rest_framework import routers

from products import views

router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet)
urlpatterns = [
    path("",include(router.urls))
]
