from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import Supplier, PurchaseOrder, Warehouse, InventoryLog, InventoryAlert


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class POSerializer(serializers.ModelSerializer):
    supplier_id = serializers.IntegerField(source='supplier.id', read_only=True, allow_null=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'supplier_id', 'total_amount', 'status', 'order_date', 'received_date', 'notes']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAlert
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'inventory_service', 'timestamp': datetime.utcnow().isoformat()})


# ── SUPPLIER ────────────────────────────────────────────
@api_view(['GET'])
def list_suppliers(request):
    return Response(SupplierSerializer(Supplier.objects.all(), many=True).data)


@api_view(['POST'])
def create_supplier(request):
    s = SupplierSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    supplier = s.save()
    return Response(SupplierSerializer(supplier).data, status=201)


# ── PURCHASE ORDER ──────────────────────────────────────
@api_view(['GET'])
def list_pos(request):
    pos = PurchaseOrder.objects.order_by('-order_date')
    return Response(POSerializer(pos, many=True).data)


@api_view(['POST'])
def create_po(request):
    data = request.data
    supplier = Supplier.objects.filter(id=data.get('supplier_id')).first()
    po = PurchaseOrder.objects.create(
        supplier=supplier,
        notes=data.get('notes')
    )
    return Response(POSerializer(po).data, status=201)


@api_view(['PATCH'])
def update_po_status(request, po_id):
    po = PurchaseOrder.objects.filter(id=po_id).first()
    if not po:
        return Response({'detail': 'Không tìm thấy đơn nhập hàng'}, status=404)
    status_val = request.data.get('status', request.query_params.get('status', ''))
    po.status = status_val
    if status_val == 'RECEIVED':
        from django.utils import timezone
        po.received_date = timezone.now()
    po.save()
    return Response({'po_id': po_id, 'status': status_val})


# ── WAREHOUSE ───────────────────────────────────────────
@api_view(['GET'])
def list_warehouses(request):
    return Response(WarehouseSerializer(Warehouse.objects.all(), many=True).data)


@api_view(['POST'])
def create_warehouse(request):
    s = WarehouseSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    w = s.save()
    return Response(WarehouseSerializer(w).data, status=201)


# ── INVENTORY LOGS ──────────────────────────────────────
@api_view(['GET'])
def list_logs(request):
    limit = int(request.query_params.get('limit', 50))
    logs = InventoryLog.objects.order_by('-timestamp')[:limit]
    return Response(LogSerializer(logs, many=True).data)


@api_view(['POST'])
def add_log(request):
    s = LogSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    log = s.save()
    return Response(LogSerializer(log).data, status=201)


# ── ALERTS ──────────────────────────────────────────────
@api_view(['GET'])
def list_alerts(request):
    alerts = InventoryAlert.objects.filter(is_resolved=False)
    return Response(AlertSerializer(alerts, many=True).data)


@api_view(['POST'])
def create_alert(request):
    s = AlertSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    alert = s.save()
    return Response(AlertSerializer(alert).data, status=201)


@api_view(['PATCH'])
def resolve_alert(request, alert_id):
    alert = InventoryAlert.objects.filter(id=alert_id).first()
    if not alert:
        return Response({'detail': 'Không tìm thấy cảnh báo'}, status=404)
    alert.is_resolved = True
    alert.save()
    return Response({'alert_id': alert_id, 'resolved': True})
