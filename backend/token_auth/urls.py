    
from django.urls import path
from token_auth.views import CustomerSignUpView, CustomerLogInView, CustomerLogOutView, CustomerChangeDetailsView, CustomerChangePasswordView


urlpatterns = [
    # path('', CustomerTokenPairView.as_view(), name='token_obtain_pair'),
    # path('refresh/', CustomerTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomerSignUpView.as_view(), name='auth_register'),
    path('login/', CustomerLogInView.as_view(), name='auth-login'),
    path('logout/',CustomerLogOutView.as_view(), name='auth-logout'),
    path('change-details/',CustomerChangeDetailsView.as_view(), name='auth-change-details'),
    path('change-password/',CustomerChangePasswordView.as_view(), name='change-password')   
]