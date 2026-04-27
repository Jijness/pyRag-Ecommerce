from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'supplier'


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, db_column='supplier_id')
    total_amount = models.FloatField(default=0)
    status = models.CharField(max_length=50, default='DRAFT')
    order_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'purchase_order'


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, db_column='order_id')
    book_id = models.IntegerField()
    quantity = models.IntegerField()
    unit_cost = models.FloatField()

    class Meta:
        db_table = 'purchase_order_item'


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'warehouse'


class InventoryLog(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, db_column='warehouse_id')
    book_id = models.IntegerField()
    change_type = models.CharField(max_length=50)  # IN | OUT | ADJUSTMENT
    quantity = models.IntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_log'


class InventoryAlert(models.Model):
    book_id = models.IntegerField()
    threshold = models.IntegerField(default=10)
    current_stock = models.IntegerField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_alert'
