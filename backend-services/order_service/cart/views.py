from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer

def get_or_create_cart(customer_id):
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if not cart:
        cart = Cart.objects.create(customer_id=customer_id)
    return cart

@api_view(['GET'])
def view_cart(request, customer_id):
    cart = get_or_create_cart(customer_id)
    return Response(CartSerializer(cart).data)

@api_view(['POST'])
def add_to_cart(request, customer_id):
    cart = get_or_create_cart(customer_id)
    data = request.data
    product_id = data.get('product_id') or data.get('book_id')
    quantity = data.get('quantity', 1)
    unit_price = data.get('unit_price')

    item = CartItem.objects.filter(cart=cart, book_id=product_id).first()
    if item:
        item.quantity += quantity
        item.save()
    else:
        CartItem.objects.create(
            cart=cart, book_id=product_id, quantity=quantity, unit_price=unit_price
        )
    return Response({"message": "Đã thêm vào giỏ", "cart_id": cart.id})

@api_view(['PATCH'])
def update_cart_quantity(request, customer_id, item_id):
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if not cart:
        return Response({"detail": "Không tìm thấy giỏ hàng"}, status=404)
    item = CartItem.objects.filter(id=item_id, cart=cart).first()
    if not item:
        return Response({"detail": "Không tìm thấy sản phẩm trong giỏ"}, status=404)
    
    quantity = request.GET.get('quantity')
    if quantity is None:
        quantity = request.data.get('quantity')
    quantity = int(quantity)
    
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return Response({"message": "Đã cập nhật", "item_id": item_id, "quantity": max(quantity, 0)})

@api_view(['DELETE'])
def remove_cart_item(request, customer_id, item_id):
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if not cart:
        return Response({"detail": "Không tìm thấy giỏ hàng"}, status=404)
    item = CartItem.objects.filter(id=item_id, cart=cart).first()
    if not item:
        return Response({"detail": "Không tìm thấy sản phẩm trong giỏ"}, status=404)
    item.delete()
    return Response(status=204)

@api_view(['DELETE'])
def clear_cart(request, customer_id):
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if cart:
        CartItem.objects.filter(cart=cart).delete()
    return Response(status=204)

@api_view(['GET'])
def cart_summary(request, customer_id):
    cart = Cart.objects.filter(customer_id=customer_id, is_active=True).first()
    if not cart:
        return Response({"item_count": 0, "total_price": 0.0, "cart_id": None})
    items = cart.items.all()
    total = sum([(i.unit_price or 0) * i.quantity for i in items])
    count = sum([i.quantity for i in items])
    return Response({"item_count": count, "total_price": round(total, 2), "cart_id": cart.id})
