import httpx
import logging
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jose import jwt, JWTError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger("api_gateway")

# ── Config ────────────────────────────────────────────
SECRET_KEY = "learnmart-secret-key-2024-very-secure"
ALGORITHM  = "HS256"

MAX_REQUESTS   = 60
WINDOW_SECONDS = 60

UPSTREAM = {
    "/auth/":          "http://user_service:8001",
    "/products/":      "http://product_service:8002",
    "/books/":         "http://product_service:8002",
    "/cart/":          "http://cart_service:8003",
    "/orders/":        "http://order_service:8004",
    "/payments/":      "http://payment_service:8005",
    "/shipping/":      "http://shipping_service:8006",
    "/ai/":            "http://ai_service:8007",
}

PUBLIC_PATHS = {
    "/auth/login/customer",
    "/auth/login/staff",
    "/auth/register/customer",
    "/auth/register/staff",
    "/health",
    "/",
}

STAFF_ONLY_PREFIXES = [
    "/staff/",
    "/inventory/",
    "/analytics/",
    "/marketing/",
]

# ── Rate-limit store ─────────────────────────────────
_rate_store = defaultdict(list)

def check_rate_limit(ip):
    now = time.time()
    window_start = now - WINDOW_SECONDS
    _rate_store[ip] = [t for t in _rate_store[ip] if t > window_start]
    if len(_rate_store[ip]) >= MAX_REQUESTS:
        return False
    _rate_store[ip].append(now)
    return True

# ── JWT helper ────────────────────────────────────────
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
@permission_classes([AllowAny])
def gateway_proxy(request, path=""):
    path = "/" + path
    client_ip = request.META.get('REMOTE_ADDR', 'unknown')
    method = request.method

    # 1. Rate limiting
    if not check_rate_limit(client_ip):
        return JsonResponse({"detail": "Quá nhiều yêu cầu"}, status=429)

    # 2. JWT Authentication
    user_payload = None
    is_public = path in PUBLIC_PATHS or any(path.startswith(p) for p in ["/auth/login", "/auth/register"])

    if not is_public:
        auth_header = request.headers.get("Authorization", "")
        raw_token = None
        if auth_header.startswith("Bearer "):
            raw_token = auth_header[7:]
        
        if not raw_token:
            return JsonResponse({"detail": "Yêu cầu xác thực. Vui lòng cung cấp JWT token."}, status=401)
        
        user_payload = decode_token(raw_token)
        if not user_payload:
            return JsonResponse({"detail": "Token không hợp lệ hoặc đã hết hạn"}, status=401)

    # 3. RBAC
    if user_payload:
        user_type = user_payload.get("user_type", "")
        if any(path.startswith(p) for p in STAFF_ONLY_PREFIXES):
            if user_type != "staff":
                return JsonResponse({"detail": "Bạn không có quyền truy cập endpoint này"}, status=403)

    # 4. Route matching
    upstream_base = None
    upstream_path = path
    for prefix, base in UPSTREAM.items():
        if path.startswith(prefix):
            upstream_base = base
            upstream_path = path[len(prefix)-1:]
            break

    if not upstream_base:
        if path == "/":
            return JsonResponse({
                "service": "LearnMart API Gateway (Django)",
                "version": "2.1.0",
                "routes": list(UPSTREAM.keys())
            })
        return JsonResponse({"detail": f"Route không tồn tại: {path}"}, status=404)

    # 5. Forward request
    target_url = upstream_base + upstream_path
    query_params = request.GET.urlencode()
    if query_params:
        target_url += "?" + query_params

    excluded = {"host", "content-length", "transfer-encoding", "connection"}
    fwd_headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded}

    if user_payload:
        fwd_headers["X-User-Id"]   = str(user_payload.get("sub", ""))
        fwd_headers["X-User-Type"] = user_payload.get("user_type", "")
        fwd_headers["X-User-Role"] = user_payload.get("role", "")
        fwd_headers["X-User-Name"] = user_payload.get("name", "")

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.request(
                method=method,
                url=target_url,
                headers=fwd_headers,
                content=request.body,
            )
        
        response = HttpResponse(
            content=resp.content,
            status=resp.status_code,
            content_type=resp.headers.get("content-type"),
        )
        for k, v in resp.headers.items():
            if k.lower() not in {"content-type", "content-length", "transfer-encoding"}:
                response[k] = v
        return response

    except httpx.RequestError as e:
        logger.error(f"Proxy error: {e}")
        return JsonResponse({"detail": "Service không khả dụng"}, status=502)

def health_check(request):
    return JsonResponse({"status": "ok", "service": "api_gateway", "timestamp": datetime.utcnow().isoformat()})
