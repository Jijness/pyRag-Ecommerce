from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from .publisher import publish_order_created
import httpx
import logging

logger = logging.getLogger(__name__)

# Base URL cho các Microservices (theo cấu hình của Docker network)
CART_SERVICE_URL = "http://cart_service:8003/cart"

@api_view(['POST'])
def checkout(request):
    data = request.data
    customer_id = data.get('customer_id')
    
    if not customer_id:
        return Response({"detail": "Thiếu customer_id"}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Gọi HTTP sang Cart Service để lấy giỏ hàng
    try:
        # Giả sử cart_service trả về data. Giỏ hàng có id theo customer_id hoặc cần một API list.
        # Ở đây ta gọi /cart/?customer_id=... hoặc /cart/<customer_id>
        resp = httpx.get(f"{CART_SERVICE_URL}/?customer_id={customer_id}", timeout=5.0)
        resp.raise_for_status()
        carts = resp.json()
        if not carts or not isinstance(carts, list) or len(carts) == 0:
            return Response({"detail": "Giỏ hàng trống hoặc không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_data = carts[0]
        items = cart_data.get('items', [])
        if not items:
            return Response({"detail": "Giỏ hàng không có sản phẩm"}, status=status.HTTP_400_BAD_REQUEST)
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch cart: {e}")
        return Response({"detail": "Lỗi kết nối đến Cart Service"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # 2. Tính toán tổng tiền
    total_price = sum([(i.get('unit_price', 0) or 0) * i.get('quantity', 1) for i in items])
    total_qty = sum([i.get('quantity', 1) for i in items])
    ship_method = data.get('ship_method', 'standard')
    fee = 30000 if ship_method == "fast" else 15000
    
    # 3. Tạo Order Record (Order Database)
    order = Order.objects.create(
        customer_id=customer_id,
        coupon_code=data.get('coupon_code'),
        total_price=total_price + fee,
        total_quantity=total_qty,
        note=data.get('note'),
        status="PENDING",
        saga_status="INITIATED", # Trạng thái Saga ban đầu
        saga_step="order_created",
    )
    
    for item in items:
        OrderItem.objects.create(
            order=order,
            book_id=item.get('book_id'),
            book_title=item.get('book_title'),
            price=item.get('unit_price', 0) or 0,
            quantity=item.get('quantity', 1)
        )
        
    # 4. Gửi RabbitMQ Event (Saga Orchestration) -> Payment & Shipping services
    publish_order_created(
        order_id=order.id,
        customer_id=customer_id,
        total_price=total_price + fee,
        pay_method=data.get('pay_method', 'cod'),
        ship_method=ship_method
    )
    
    # 5. Clear Cart (Gọi HTTP DELETE / PATCH sang Cart Service)
    try:
        cart_id = cart_data.get('id')
        if cart_id:
            httpx.patch(f"{CART_SERVICE_URL}/{cart_id}/", json={"is_active": False}, timeout=5.0)
    except Exception as e:
        logger.warning(f"Failed to clear cart: {e}")
    
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def my_orders(request, customer_id):
    orders = Order.objects.filter(customer_id=customer_id).order_by('-date')
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['GET'])
def all_orders(request):
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))
    status_filter = request.GET.get('status', '')
    
    query = Order.objects.all().order_by('-date')
    if status_filter:
        query = query.filter(status=status_filter)
        
    orders = query[skip:skip+limit]
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['GET'])
def get_order(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return Response(status=404)
    return Response(OrderSerializer(order).data)

@api_view(['GET'])
def order_items(request, order_id):
    items = OrderItem.objects.filter(order_id=order_id)
    return Response(OrderItemSerializer(items, many=True).data)

@api_view(['PATCH'])
def update_status(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return Response(status=404)
    new_status = request.data.get('status') or request.GET.get('status')
    if new_status:
        order.status = new_status
        order.save()
    return Response({"message": "Cập nhật thành công", "order_id": order.id, "status": order.status})

@api_view(['GET'])
def stats_summary(request):
    total = Order.objects.count()
    completed = Order.objects.filter(status="COMPLETED").count()
    revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return Response({
        "total_orders": total,
        "completed_orders": completed,
        "total_revenue": round(revenue, 2),
        "avg_order_value": round(revenue / total, 2) if total > 0 else 0
    })
