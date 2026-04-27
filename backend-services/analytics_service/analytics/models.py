from django.db import models


class SalesSummary(models.Model):
    date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.FloatField(default=0)
    avg_order_value = models.FloatField(default=0)
    top_product_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'sales_summaries'


class SearchHistory(models.Model):
    customer_id = models.IntegerField()
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)
    result_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'search_histories'


class RecentlyViewed(models.Model):
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recently_viewed'
