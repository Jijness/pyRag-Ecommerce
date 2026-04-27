from django.db import models


class Notification(models.Model):
    customer_id = models.IntegerField()
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, default='general')

    class Meta:
        db_table = 'notifications'
