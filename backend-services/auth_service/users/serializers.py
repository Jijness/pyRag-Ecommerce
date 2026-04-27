from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_active', 'user_type']
        read_only_fields = ['id', 'is_active', 'user_type']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'role', 'is_active', 'user_type']
        read_only_fields = ['id', 'is_active', 'user_type']

class RegisterCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email đã được sử dụng")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # use email as username for customers
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            user_type='customer'
        )
        return user

class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'role']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username đã tồn tại")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            role=validated_data.get('role', 'staff'),
            user_type='staff'
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        token['name'] = user.name
        if user.role:
            token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['access_token'] = data.pop('access') # Rename to match old API format
        data['user_type'] = self.user.user_type
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        if self.user.role:
            data['role'] = self.user.role
        return data
