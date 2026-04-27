from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.TextField(blank=True, null=True)
    link_url = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'banners'


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product_ids = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'collections'


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'blog_posts'
