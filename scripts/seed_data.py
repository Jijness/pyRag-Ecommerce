"""Seed demo data for LearnMart marketplace."""
from __future__ import annotations

import io
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

from seed_catalog import DEFAULT_BRANDS, DEFAULT_CATEGORIES, DEFAULT_PRODUCT_TYPES, DEFAULT_PRODUCTS

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


BASE = {
    "auth": "http://localhost:8001",
    "product": "http://localhost:8002",
    "cart": "http://localhost:8003",
    "order": "http://localhost:8004",
    "payment": "http://localhost:8005",
    "shipping": "http://localhost:8006",
    "ai": "http://localhost:8007",
}


def log(message):
    print(message, flush=True)


def log_step(message):
    log(f"[STEP] {message}")


def log_ok(message):
    log(f"[OK] {message}")


def log_warn(message):
    log(f"[WARN] {message}")


def post(url, body, label="", retries=10, delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, json=body, timeout=10)
            if response.status_code in (200, 201):
                if label:
                    log_ok(f"{label}")
                return response.json() if response.content else None
            if response.status_code in (400, 409):
                try:
                    data = response.json()
                except Exception:
                    data = {"detail": response.text}
                log_warn(f"[{response.status_code}] {label}: {data}")
                return None
            last_error = RuntimeError(f"{response.status_code} {response.text[:300]}")
        except Exception as exc:
            last_error = exc
            if label:
                log_warn(f"{label} failed on attempt {attempt}/{retries}: {exc}")
        time.sleep(delay)
    log_warn(f"ERR {label}: {last_error}")
    return None


def get(url, retries=10, delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            if response.ok:
                return response.json()
            last_error = RuntimeError(f"{response.status_code} {response.text[:300]}")
        except Exception as exc:
            last_error = exc
            log_warn(f"GET failed on attempt {attempt}/{retries}: {url} -> {exc}")
        time.sleep(delay)
    log_warn(f"ERR GET {url}: {last_error}")
    return None


def wait_services():
    health_urls = [
        f"{BASE['auth']}/health",
        f"{BASE['product']}/health",
        f"{BASE['cart']}/health",
        f"{BASE['order']}/health",
    ]
    for url in health_urls:
        log_step(f"Waiting for {url}")
        ok = False
        for attempt in range(1, 41):
            try:
                response = requests.get(url, timeout=5)
                if response.ok:
                    ok = True
                    log_ok(f"Health ready: {url}")
                    break
            except Exception:
                pass
            time.sleep(2)
        if not ok:
            log_warn(f"Health not ready: {url}")


def ensure_customer():
    post(
        f"{BASE['auth']}/register/customer",
        {"name": "Khách Hàng Demo", "email": "demo@learnmart.vn", "password": "demo123"},
        "register customer",
        retries=2,
        delay=1,
    )
    token = post(
        f"{BASE['auth']}/login/customer",
        {"email": "demo@learnmart.vn", "password": "demo123"},
        "login customer",
    )
    if not token:
        return 1
    me = get(f"{BASE['auth']}/me?token={token['access_token']}") or {}
    return me.get("user_id", 1)


def ensure_staff():
    post(
        f"{BASE['auth']}/register/staff",
        {"name": "Admin Staff", "username": "admin", "password": "admin123", "role": "ADMIN"},
        "register staff",
        retries=2,
        delay=1,
    )
    token = post(
        f"{BASE['auth']}/login/staff",
        {"username": "admin", "password": "admin123"},
        "login staff",
    )
    if not token:
        return 1
    me = get(f"{BASE['auth']}/me?token={token['access_token']}") or {}
    return me.get("user_id", 1)


def get_slug_map(items):
    return {item["slug"]: item["id"] for item in items if "slug" in item}


def build_product_payloads(category_map, type_map, brand_map):
    return [
        {
            "name": product["name"],
            "sku": product["sku"],
            "price": product["price"],
            "stock_quantity": product["stock_quantity"],
            "category_id": category_map.get(product["category_slug"]),
            "product_type_id": type_map.get(product["product_type_slug"]),
            "brand_id": brand_map.get(product["brand_slug"]),
            "description": product["description"],
            "attributes": product["attributes"],
        }
        for product in DEFAULT_PRODUCTS
    ]


def main():
    wait_services()
    log("\n=== Seeding Accounts ===")
    customer_id = ensure_customer()
    staff_id = ensure_staff()
    log_ok(f"Accounts ready: customer_id={customer_id}, staff_id={staff_id}")

    log("\n=== Seeding Catalog ===")
    for index, category in enumerate(DEFAULT_CATEGORIES, start=1):
        log_step(f"Category {index}/{len(DEFAULT_CATEGORIES)}: {category['name']}")
        post(f"{BASE['product']}/categories", category, category["name"], retries=2, delay=1)

    for index, product_type in enumerate(DEFAULT_PRODUCT_TYPES, start=1):
        log_step(f"Product type {index}/{len(DEFAULT_PRODUCT_TYPES)}: {product_type['name']}")
        post(f"{BASE['product']}/product-types", product_type, product_type["name"], retries=2, delay=1)

    for index, brand in enumerate(DEFAULT_BRANDS, start=1):
        log_step(f"Brand {index}/{len(DEFAULT_BRANDS)}: {brand['name']}")
        post(f"{BASE['product']}/brands", brand, brand["name"], retries=2, delay=1)

    categories = get(f"{BASE['product']}/categories") or []
    product_types = get(f"{BASE['product']}/product-types") or []
    brands = get(f"{BASE['product']}/brands") or []
    category_map = get_slug_map(categories)
    type_map = get_slug_map(product_types)
    brand_map = get_slug_map(brands)

    catalog = build_product_payloads(category_map, type_map, brand_map)
    product_ids = []
    for index, item in enumerate(catalog, start=1):
        log_step(f"Product {index}/{len(catalog)}: {item['name']}")
        created = post(f"{BASE['product']}/products", item, item["name"], retries=2, delay=1)
        if created:
            product_ids.append(created["id"])

    log("\nSeed completed for Auth and Product.")


if __name__ == "__main__":
    main()
