from rest_framework import serializers
from .models import Category, Product, Review, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    title = serializers.CharField(source='name', read_only=True)
    stock_quantity = serializers.IntegerField(source='stock', read_only=True)
    description = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    rating_avg = serializers.FloatField(default=0.0, read_only=True)
    rating_count = serializers.IntegerField(default=0, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'name', 'category', 'category_name', 'price', 'stock_quantity', 'stock', 'description', 'attributes', 'author_name', 'cover_image_url', 'rating_avg', 'rating_count']

    def get_description(self, obj):
        return obj.attributes.get('description', '')

    def get_author_name(self, obj):
        return obj.attributes.get('author') or obj.attributes.get('brand') or obj.category.name

    def get_cover_image_url(self, obj):
        return obj.attributes.get('cover_image_url')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

