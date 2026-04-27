from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime

from .serializers import (
    CustomerSerializer, StaffSerializer,
    RegisterCustomerSerializer, RegisterStaffSerializer,
    CustomTokenObtainPairSerializer
)

User = get_user_model()

# ════════════════════════════════════════════════════════
# HEALTH & METRICS
# ════════════════════════════════════════════════════════
class HealthView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"status": "ok", "service": "auth_service", "timestamp": datetime.utcnow().isoformat()})

class MetricsView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        total_customers = User.objects.filter(user_type='customer').count()
        total_staff = User.objects.filter(user_type='staff').count()
        active_customers = User.objects.filter(user_type='customer', is_active=True).count()
        return Response({
            "service": "auth_service",
            "total_customers": total_customers,
            "active_customers": active_customers,
            "total_staff": total_staff,
        })

# ════════════════════════════════════════════════════════
# CUSTOMER ENDPOINTS
# ════════════════════════════════════════════════════════
class RegisterCustomerView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterCustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        out_serializer = CustomerSerializer(user)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

class LoginCustomerView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # The old API used 'email' instead of 'username' for customer login payload
        if 'email' in request.data:
            request.data['username'] = request.data['email']
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception:
            return Response({"detail": "Sai email hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(username=request.data.get('username'))
        if user.user_type != 'customer':
            return Response({"detail": "Sai email hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class CustomerListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='customer')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny] # In old code this was no permission enforced

class CustomerDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(user_type='customer')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

# ════════════════════════════════════════════════════════
# STAFF ENDPOINTS
# ════════════════════════════════════════════════════════
class RegisterStaffView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStaffSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        out_serializer = StaffSerializer(user)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

class LoginStaffView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(username=request.data.get('username'))
        if user.user_type != 'staff':
            return Response({"detail": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class StaffListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='staff')
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

class StaffDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(user_type='staff')
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

# ════════════════════════════════════════════════════════
# TOKEN VERIFY
# ════════════════════════════════════════════════════════
class VerifyTokenView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Cần cung cấp token"}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_token)
            return Response({
                "valid": True,
                "user_id": user.id,
                "user_type": user.user_type,
                "role": user.role,
                "name": user.name
            })
        except Exception:
            return Response({"detail": "Token không hợp lệ hoặc đã hết hạn"}, status=status.HTTP_401_UNAUTHORIZED)

class MeView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        token = request.query_params.get('token')
        auth_header = request.headers.get('Authorization')
        
        raw_token = token
        if not raw_token and auth_header and auth_header.startswith('Bearer '):
            raw_token = auth_header[7:]
            
        if not raw_token:
            return Response({"detail": "Cần cung cấp token"}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            validated_token = JWTAuthentication().get_validated_token(raw_token)
            user = JWTAuthentication().get_user(validated_token)
            return Response({
                "user_id": user.id,
                "user_type": user.user_type,
                "role": user.role,
                "name": user.name
            })
        except Exception:
            return Response({"detail": "Token không hợp lệ hoặc đã hết hạn"}, status=status.HTTP_401_UNAUTHORIZED)
