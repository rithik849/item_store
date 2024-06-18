    
from django.urls import path
from user_auth.views import CustomerSignUpView, CustomerLogInView, CustomerLogOutView, CustomerChangeDetailsView, CustomerChangePasswordView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', CustomerSignUpView.as_view(), name='auth_register'),
    path('login/', CustomerLogInView.as_view(), name='auth-login'),
    path('logout/',CustomerLogOutView.as_view(), name='auth-logout'),
    path('change-details/',CustomerChangeDetailsView.as_view(), name='auth-change-details'),
    path('change-password/',CustomerChangePasswordView.as_view(), name='change-password')   
]