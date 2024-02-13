from django.urls import include, path

from products import views

urlpatterns = [
    path("<int:pk>/",include(views.ProductViewSet))
]
