from rest_framework import serializers
from .models import Category, Brand, ProductType, Product, Review, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False)
    brand_id = serializers.IntegerField(required=False)
    product_type_id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
