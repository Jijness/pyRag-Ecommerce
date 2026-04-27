from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('health', views.HealthView.as_view(), name='health'),
    path('metrics', views.MetricsView.as_view(), name='metrics'),
    
    path('register/customer', views.RegisterCustomerView.as_view(), name='register_customer'),
    path('login/customer', views.LoginCustomerView.as_view(), name='login_customer'),
    path('customers', views.CustomerListView.as_view(), name='list_customers'),
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='get_customer'),
    
    path('register/staff', views.RegisterStaffView.as_view(), name='register_staff'),
    path('login/staff', views.LoginStaffView.as_view(), name='login_staff'),
    path('staff', views.StaffListView.as_view(), name='list_staff'),
    path('staff/<int:pk>', views.StaffDetailView.as_view(), name='get_staff'),
    
    path('verify-token', views.VerifyTokenView.as_view(), name='verify_token'),
    path('me', views.MeView.as_view(), name='me'),
    
    # New endpoint for token refresh
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
