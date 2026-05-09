import logging
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddItemSerializer, UpdateItemSerializer

logger = logging.getLogger(__name__)


def _get_or_create_cart(customer_id=None, session_id=None):
    """Domain logic: Lấy cart đang active hoặc tạo mới."""
    if customer_id:
        cart, _ = Cart.objects.get_or_create(
            customer_id=customer_id, is_active=True,
            defaults={'session_id': None}
        )
    elif session_id:
        cart, _ = Cart.objects.get_or_create(
            session_id=session_id, is_active=True,
            defaults={'customer_id': None}
        )
    else:
        cart = Cart.objects.create()
    return cart


class CartDetailView(APIView):
    """
    GET /cart/   — Xem giỏ hàng hiện tại.
    Actor: Customer (customer_id header) hoặc Guest (session_id header).
    """
    def get(self, request):
        customer_id = request.headers.get('X-Customer-Id')
        session_id = request.headers.get('X-Session-Id')
        cart = _get_or_create_cart(customer_id, session_id)
        return Response(CartSerializer(cart).data)


class CartItemListView(APIView):
    """
    POST /cart/items   — Thêm sản phẩm vào giỏ.
    Nếu sản phẩm đã có → cộng dồn quantity.
    """
    def post(self, request):
        customer_id = request.headers.get('X-Customer-Id')
        session_id = request.headers.get('X-Session-Id')

        ser = AddItemSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = _get_or_create_cart(customer_id, session_id)
        product_id = ser.validated_data['product_id']
        qty = ser.validated_data['quantity']

        item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id,
            defaults={'quantity': qty}
        )
        if not created:
            item.quantity += qty
            item.save()

        logger.info(f"[cart_service] Added product {product_id} x{qty} to cart {cart.pk}")
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    """
    PATCH /cart/items/<item_id>   — Cập nhật quantity.
    DELETE /cart/items/<item_id>  — Xóa item.
    """
    def patch(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id)
        ser = UpdateItemSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = ser.validated_data['quantity']
        item.save()
        return Response(CartItemSerializer(item).data)

    def delete(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id)
        cart_id = item.cart_id
        item.delete()
        cart = Cart.objects.get(pk=cart_id)
        return Response(CartSerializer(cart).data)


class CartClearView(APIView):
    """
    DELETE /cart/clear   — Xóa toàn bộ giỏ hàng.
    """
    def delete(self, request):
        customer_id = request.headers.get('X-Customer-Id')
        try:
            cart = Cart.objects.get(customer_id=customer_id, is_active=True)
            cart.items.all().delete()
            return Response({"message": "Cart cleared."})
        except Cart.DoesNotExist:
            return Response({"message": "No active cart."})


class CartDeactivateView(APIView):
    """
    PATCH /cart/<cart_id>/deactivate
    Internal endpoint — Order Service gọi sau checkout thành công.
    """
    def patch(self, request, cart_id):
        cart = get_object_or_404(Cart, pk=cart_id, is_active=True)
        cart.is_active = False
        cart.save()
        logger.info(f"[cart_service] Cart {cart_id} deactivated after checkout.")
        return Response({"message": f"Cart {cart_id} deactivated."})
