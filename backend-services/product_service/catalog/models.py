from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'brand'

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'product_type'

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='products', null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, related_name='products', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    attributes = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    customer_id = models.IntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rating'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer_id = models.IntegerField()
    title = models.CharField(max_length=255, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
