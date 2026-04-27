from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Order, OrderItem
from payment.models import Payment
from shipping.models import Shipping
from cart.models import Cart, CartItem
from .serializers import OrderSerializer, OrderItemSerializer

@api_view(['POST'])
def checkout(request):
    data = request.data
    customer_id = data.get('customer_id')
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if not cart:
        return Response({"detail": "Giỏ hàng trống hoặc không tồn tại"}, status=400)
    
    items = cart.items.all()
    if not items:
        return Response({"detail": "Giỏ hàng không có sản phẩm"}, status=400)
        
    total_price = sum([(i.unit_price or 0) * i.quantity for i in items])
    total_qty = sum([i.quantity for i in items])
    ship_method = data.get('ship_method', 'standard')
    fee = 30000 if ship_method == "fast" else 15000
    
    order = Order.objects.create(
        customer_id=customer_id,
        coupon_code=data.get('coupon_code'),
        total_price=total_price + fee,
        total_quantity=total_qty,
        note=data.get('note'),
        status="PENDING",
        saga_status="CONFIRMED",
        saga_step="direct_checkout",
    )
    
    for item in items:
        OrderItem.objects.create(
            order=order,
            book_id=item.book_id,
            price=item.unit_price or 0,
            quantity=item.quantity
        )
        
    Shipping.objects.create(order=order, method=ship_method, fee=fee)
    Payment.objects.create(order=order, method=data.get('pay_method'), amount=total_price + fee)
    
    cart.is_active = False
    cart.save()
    
    # Event could be published here via Celery or directly via pika
    # (Leaving out RabbitMQ direct call for simplicity in Django refactor)
    
    return Response(OrderSerializer(order).data, status=201)

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
    new_status = request.GET.get('status')
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
