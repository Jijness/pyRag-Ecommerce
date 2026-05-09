from __future__ import annotations

import re
import unicodedata
from typing import Any

from .behavior_model import BehaviorModel
from .sequence_behavior_model import SequenceBehaviorModel
from .data_fetcher import ServiceClient
from .graph_store import GraphKBStore
from .kb_store import KBStore

CATEGORY_ALIASES = {
    "SÃ¡ch": ["sach", "book", "truyen", "self help", "tieu thuyet", "fantasy", "van hoc", "doc sach", "nguoi doc", "moi doc"],
    "Äiá»‡n thoáº¡i": ["dien thoai", "phone", "iphone", "samsung", "smartphone", "di dong"],
    "Laptop": ["laptop", "may tinh xach tay", "macbook", "notebook"],
    "Thá»i trang Nam": ["thoi trang nam", "quan ao nam", "ao thun nam", "quan nam"],
    "Thá»i trang Ná»¯": ["thoi trang nu", "quan ao nu", "ao nu", "vay", "dam"],
    "Äá»“ gia dá»¥ng": ["do gia dung", "bep", "nha cua", "noi", "chao", "may xay"],
    "Äá»“ chÆ¡i": ["do choi", "lego", "toy", "xep hinh", "mo hinh", "gundam", "board game"],
    "VÄƒn phÃ²ng pháº©m": ["van phong pham", "but", "vo", "so", "stationery", "highlight", "thuoc ke", "gom", "hop but"],
    "LÃ m Ä‘áº¹p": ["lam dep", "my pham", "son", "makeup", "skincare", "duong da"],
    "Sá»©c khá»e": ["suc khoe", "may do huyet ap", "thuc pham chuc nang", "vitamin"],
    "BÃ¡ch hÃ³a online": ["bach hoa", "do an", "banh keo", "nuoc uong", "sua", "mi goi"],
    "Phá»¥ kiá»‡n sá»‘": ["phu kien", "tai nghe", "headphone", "earphone", "chuot may tinh", "ban phim", "ipad", "may tinh bang", "cap sac", "usb", "webcam", "dong ho thong minh", "op lung", "kinh cuong luc"],
}

POLICY_KEYWORDS = [
    "don hang",
    "van chuyen",
    "giao hang",
    "shipping",
    "refund",
    "doi tra",
    "coupon",
    "voucher",
    "thanh vien",
    "membership",
    "cart",
    "gio hang",
    "checkout",
    "thanh toan",
    "payment",
    "chinh sach",
    "bao hanh"
]

PRODUCT_KEYWORDS = [
    "goi y",
    "nen mua",
    "ngan sach",
    "bao nhieu",
    "mua gi",
    "san pham",
    "danh muc",
    "qua",
    "do dung",
    "phu kien",
    "dien thoai",
    "laptop",
    "tai nghe",
    "ban phim"
]

PURCHASE_KEYWORDS = ["mua", "muon mua", "dat mua", "can mua", "tim mua", "chot", "lay"]
AVAILABILITY_KEYWORDS = ["co nhung loai", "co nhung mat hang", "shop co nhung", "co ban", "shop co", "cua hang co", "ben minh co", "co khong", "shop ban", "dang ban"]
CATALOG_LIST_KEYWORDS = ["loai mat hang", "mat hang nao", "ban nhung gi", "co nhung gi", "san pham nao", "hang hoa gi", "shop co gi"]


def _searchable_text(value: str) -> str:
    value = (value or "").replace("Ä‘", "d").replace("Ä", "D")
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def parse_money_to_vnd(text: str) -> dict[str, int | str] | None:
    normalized = (
        _searchable_text(text)
        .replace("trieu", "000000")
        .replace("nghin", "000")
        .replace("ngan", "000")
        .replace("k", "000")
    )
    nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[\.,]\d+)?", normalized)]
    if not nums:
        return None

    def normalize(value: float) -> int:
        return int(value * 1000) if value < 1000 and "000" in normalized else int(value)

    if re.search(r"(tu|range|khoang)\s*\d+.*(den|-|toi)\s*\d+", normalized) and len(nums) >= 2:
        low, high = normalize(nums[0]), normalize(nums[1])
        return {"type": "range", "min": min(low, high), "max": max(low, high)}
    if any(keyword in normalized for keyword in ["duoi", "khong qua", "toi da", "under", "below"]):
        return {"type": "max", "value": normalize(nums[0])}
    if any(keyword in normalized for keyword in ["tren", "it nhat", "tro len", "at least", "from"]):
        return {"type": "min", "value": normalize(nums[0])}
    return {"type": "approx", "value": normalize(nums[0])}


def match_budget(price: float, budget: dict[str, int | str] | None) -> bool:
    if not budget:
        return True
    if budget["type"] == "min":
        return price >= int(budget["value"])
    if budget["type"] == "max":
        return price <= int(budget["value"])
    if budget["type"] == "range":
        return int(budget["min"]) <= price <= int(budget["max"])
    return abs(price - int(budget["value"])) <= 30000


def detect_categories(question: str, preferred_categories: list[str]) -> list[str]:
    q = _searchable_text(question)
    hits = [category for category, aliases in CATEGORY_ALIASES.items() if any(alias in q for alias in aliases)]
    if not hits:
        hits.extend(preferred_categories[:3])
    return list(dict.fromkeys(hits))


def detect_categories_strict(question: str) -> list[str]:
    q = _searchable_text(question)
    hits = [category for category, aliases in CATEGORY_ALIASES.items() if any(alias in q for alias in aliases)]
    return list(dict.fromkeys(hits))


def classify_intent(question: str) -> str:
    q = _searchable_text(question)
    if any(keyword in q for keyword in CATALOG_LIST_KEYWORDS):
        return "catalog_list"
    if any(keyword in q for keyword in AVAILABILITY_KEYWORDS):
        return "availability_query"
    if any(keyword in q for keyword in PURCHASE_KEYWORDS):
        return "purchase_request"
    if any(keyword in q for keyword in POLICY_KEYWORDS):
        return "policy"
    if any(keyword in q for keyword in PRODUCT_KEYWORDS) or detect_categories_strict(question):
        return "product_recommendation"
    return "general"


def find_explicit_product(question: str, products: list[dict[str, Any]], target_categories: list[str] = None) -> tuple[dict[str, Any] | None, bool]:
    q_norm = _searchable_text(question)
    if not q_norm:
        return None, False

    matches: list[tuple[float, dict[str, Any]]] = []
    for product in products:
        title = str(product.get("title") or product.get("name") or "").strip()
        sku = str(product.get("sku") or "").strip()
        if not title:
            continue
        title_norm = _searchable_text(title)
        # Bá» prefix thÃ´ng dá»¥ng "sach" (vd: "SÃ¡ch Äáº¯c NhÃ¢n TÃ¢m" -> "dac nhan tam")
        stripped_title = re.sub(r"^(sach|cuon|quyen|sach giao khoa)\s+", "", title_norm).strip()
        sku_norm = _searchable_text(sku)
        score = 0.0
        is_exact = False
        for t in [title_norm, stripped_title]:
            if t and t in q_norm:
                score = max(score, 10.0 + len(t) / 100)
                is_exact = True
        if not score and sku_norm and sku_norm in q_norm:
            score = 9.0
            is_exact = True
        if not score:
            tokens = [token for token in stripped_title.split() if len(token) >= 3]
            hits = sum(1 for token in tokens if token in q_norm)
            if tokens:
                coverage = hits / len(tokens)
                # Match 1 token dÃ i >= 5 kÃ½ tá»± cÅ©ng Ä‘á»§ (tÃªn riÃªng nhÆ° "capybara", "moleskine")
                strong_hit = any(len(token) >= 5 and token in q_norm for token in tokens)
                if hits >= 2 or coverage >= 0.6 or (strong_hit and coverage >= 0.4):
                    score = 5.0 + coverage
        if score > 0:
            if target_categories:
                if product.get("category_name") in target_categories:
                    score += 20.0
                elif not is_exact:
                    continue
            matches.append((score, product, is_exact))

    if not matches:
        return None, False
    matches.sort(key=lambda item: (-item[0], float(item[1].get("price", 0) or 0)))
    return matches[0][1], matches[0][2]


def _product_text(product: dict[str, Any]) -> str:
    parts = [
        str(product.get("title") or product.get("name") or ""),
        str(product.get("description") or ""),
        str(product.get("category_name") or ""),
        str(product.get("author_name") or ""),
        str(product.get("brand_name") or ""),
    ]
    return _searchable_text(" ".join(parts))


class MarketplaceAdvisor:
    def __init__(self, base_dir: str):
        self.services = ServiceClient()
        self.behavior_model = BehaviorModel(base_dir)
        self.sequence_behavior_model = SequenceBehaviorModel(base_dir)
        self.kb = KBStore(base_dir)
        self.graph = GraphKBStore(base_dir)

    def _category_name(self, product: dict[str, Any], category_lookup: dict[Any, str]) -> str:
        return str(product.get("category_name") or category_lookup.get(product.get("category_id")) or "KhÃ¡c")

    def _category_label(self, category_name: str | None) -> str:
        if not category_name:
            return "sáº£n pháº©m"
        special_labels = {
            "SÃ¡ch": "sÃ¡ch",
            "Dá»¥ng cá»¥ há»c táº­p": "dá»¥ng cá»¥ há»c táº­p",
            "Äá»“ chÆ¡i": "Ä‘á»“ chÆ¡i",
            "GÃ³i quÃ ": "gÃ³i quÃ ",
            "Ba lÃ´": "ba lÃ´",
            "BÃ¬nh nÆ°á»›c": "bÃ¬nh nÆ°á»›c",
            "Äá»“ Ä‘iá»‡n tá»­ há»c táº­p": "Ä‘á»“ Ä‘iá»‡n tá»­ há»c táº­p",
            "Má»¹ thuáº­t": "Ä‘á»“ má»¹ thuáº­t",
            "Äá»“ trang trÃ­ bÃ n há»c": "Ä‘á»“ trang trÃ­ bÃ n há»c",
            "Äá»“ lÆ°u niá»‡m": "Ä‘á»“ lÆ°u niá»‡m",
        }
        return special_labels.get(category_name, category_name.lower())

    def _score_products(
        self,
        products: list[dict[str, Any]],
        categories: list[dict[str, Any]],
        snapshot: dict[str, Any],
        question: str,
        forced_categories: list[str] | None = None,
        graph_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        budget = parse_money_to_vnd(question)
        preferred = forced_categories or detect_categories(question, snapshot.get("preferred_categories", []))
        category_lookup = {item.get("id"): item.get("name") for item in categories}
        behavior = snapshot["behavior"]
        recent_search_terms = snapshot.get("recent_search_terms", [])
        recent_viewed_product_ids = set(snapshot.get("recent_viewed_product_ids", []))
        recent_viewed_categories = set(snapshot.get("recent_viewed_categories", []))
        graph_context = graph_context or {}
        graph_product_ids = set(graph_context.get("recent_product_ids", [])) | set(graph_context.get("query_product_ids", []))
        graph_categories = set(graph_context.get("preferred_categories", []))
        graph_brands = set(graph_context.get("preferred_brands", []))
        graph_types = set(graph_context.get("preferred_product_types", []))

        scoped_products = products
        if forced_categories:
            scoped_products = [p for p in products if self._category_name(p, category_lookup) in forced_categories]

        filtered = [p for p in scoped_products if match_budget(float(p.get("price", 0) or 0), budget)]
        candidates = filtered or scoped_products or products
        ranked: list[dict[str, Any]] = []

        for product in candidates:
            price = float(product.get("price", 0) or 0)
            stock = int(product.get("stock_quantity", 0) or 0)
            category_name = self._category_name(product, category_lookup)
            product_id = product.get("id")
            brand_name = str(product.get("brand_name") or "")
            product_type_name = str(product.get("product_type_name") or "")
            product_text = _product_text(product)
            score = 0.0
            reasons: list[str] = []

            if preferred and category_name in preferred:
                score += 3.0
                reasons.append(f"khá»›p nhÃ³m quan tÃ¢m: {category_name}")
            if category_name in graph_categories:
                score += 2.4
                reasons.append("khá»›p hÃ nh vi trÃªn graph")
            if category_name in recent_viewed_categories:
                score += 1.8
                reasons.append("cÃ¹ng nhÃ³m vá»›i sáº£n pháº©m vá»«a xem")
            if product_id in graph_product_ids:
                score += 2.8
                reasons.append("liÃªn káº¿t máº¡nh trÃªn graph")
            if brand_name and brand_name in graph_brands:
                score += 1.6
                reasons.append(f"khá»›p brand quan tÃ¢m: {brand_name}")
            if product_type_name and product_type_name in graph_types:
                score += 1.4
                reasons.append(f"khá»›p loáº¡i sáº£n pháº©m: {product_type_name}")
            if budget:
                if budget["type"] == "approx":
                    score += max(0.0, 2.5 - abs(price - int(budget["value"])) / 25000)
                else:
                    score += 2.0
                    reasons.append("náº±m trong ngÃ¢n sÃ¡ch")
            for term in recent_search_terms[-5:]:
                term_tokens = [token for token in _searchable_text(term).split() if len(token) >= 3]
                if term_tokens and any(token in product_text for token in term_tokens):
                    score += 2.2
                    reasons.append(f"khá»›p tÃ¬m kiáº¿m gáº§n Ä‘Ã¢y: {term}")
                    break
            if behavior.price_sensitivity == "high" and price <= 150000:
                score += 1.8
                reasons.append("má»©c giÃ¡ má»m")
            if behavior.purchase_intent >= 0.65 and stock > 0:
                score += 1.2
                reasons.append("cÃ³ sáºµn hÃ ng")
            if product_id in recent_viewed_product_ids:
                score -= 1.5
            if stock <= 0:
                score -= 5.0
            score += min(stock / 100, 1.0)

            ranked.append(
                {
                    "product": product,
                    "score": round(score, 3),
                    "category_name": category_name,
                    "reasons": reasons,
                }
            )

        ranked.sort(key=lambda item: (-item["score"], float(item["product"].get("price", 0) or 0)))
        return ranked

    def _dynamic_context(self, snapshot: dict[str, Any]) -> str:
        marketing = snapshot.get("marketing", {})
        cart_summary = snapshot.get("cart_summary", {})
        lines: list[str] = []
        if cart_summary.get("item_count"):
            lines.append(
                f"- Giá» hÃ ng hiá»‡n cÃ³ {cart_summary.get('item_count')} sáº£n pháº©m, táº¡m tÃ­nh {int(cart_summary.get('total_price', 0)):,}Ä‘."
            )
        for coupon in marketing.get("coupons", [])[:3]:
            if coupon.get("active", True):
                discount = coupon.get("discount_percent") or coupon.get("discount_amount")
                lines.append(f"- {coupon.get('code')}: giáº£m {discount} vá»›i Ä‘Æ¡n tá»‘i thiá»ƒu {int(coupon.get('min_order_value', 0)):,}Ä‘")
        for tier in marketing.get("tiers", [])[:2]:
            if tier.get("free_shipping"):
                lines.append(f"- Háº¡ng {tier.get('name')} cÃ³ giáº£m {tier.get('discount_percent', 0)}% vÃ  há»— trá»£ miá»…n phÃ­ ship.")
        return "\n".join(lines)

    def _format_purchase_answer(
        self,
        user_name: str,
        product: dict[str, Any],
        category_name: str,
        behavior: Any,
        snapshot: dict[str, Any],
    ) -> str:
        title = product.get("title") or product.get("name") or "Sáº£n pháº©m"
        price = int(float(product.get("price", 0) or 0))
        stock = int(product.get("stock_quantity", 0) or 0)
        description = product.get("description") or "Sáº£n pháº©m Ä‘ang cÃ³ trong catalog hiá»‡n táº¡i."
        cart_summary = snapshot.get("cart_summary", {})
        stock_line = f"CÃ²n hÃ ng ({stock} sáº£n pháº©m kháº£ dá»¥ng)." if stock > 0 else "Táº¡m háº¿t hÃ ng."
        next_action = "Báº¡n cÃ³ thá»ƒ thÃªm ngay sáº£n pháº©m nÃ y vÃ o giá» hÃ ng tá»« trang chi tiáº¿t."
        if behavior.next_best_action == "push_coupon":
            dynamic = self._dynamic_context(snapshot)
            if dynamic:
                next_action = f"Báº¡n nÃªn kiá»ƒm tra Æ°u Ä‘Ã£i trÆ°á»›c khi chá»‘t Ä‘Æ¡n:\n{dynamic}"
        elif cart_summary.get("item_count"):
            next_action = (
                f"Giá» hÃ ng hiá»‡n cÃ³ {cart_summary.get('item_count')} sáº£n pháº©m, "
                "báº¡n cÃ³ thá»ƒ vÃ o checkout Ä‘á»ƒ chá»‘t cÃ¹ng Ä‘Æ¡n."
            )
        return "\n".join(
            [
                f"MÃ¬nh Ä‘Ã£ tÃ¬m tháº¥y sáº£n pháº©m phÃ¹ há»£p cho {user_name}.",
                "",
                f"TÃªn sáº£n pháº©m: {title}",
                f"Danh má»¥c: {category_name}",
                f"GiÃ¡ hiá»‡n táº¡i: {price:,}Ä‘",
                f"TÃ¬nh tráº¡ng: {stock_line}",
                f"MÃ´ táº£ ngáº¯n: {description}",
                f"Gá»£i Ã½ tiáº¿p theo: {next_action}",
            ]
        )

    def _format_category_purchase_answer(
        self,
        user_name: str,
        category_name: str,
        ranked_products: list[dict[str, Any]],
        snapshot: dict[str, Any],
    ) -> str:
        lines = [
            f"MÃ¬nh Ä‘Ã£ tÃ¬m tháº¥y nhÃ³m sáº£n pháº©m phÃ¹ há»£p cho {user_name}.",
            "",
            f"NhÃ³m sáº£n pháº©m: {category_name}",
            "CÃ¡c lá»±a chá»n phÃ¹ há»£p nháº¥t:",
        ]
        for idx, item in enumerate(ranked_products[:3], start=1):
            product = item["product"]
            title = product.get("title") or product.get("name") or "Sáº£n pháº©m"
            price = int(float(product.get("price", 0) or 0))
            stock = int(product.get("stock_quantity", 0) or 0)
            reasons = item["reasons"][:2] or ["phÃ¹ há»£p vá»›i nhu cáº§u hiá»‡n táº¡i"]
            lines.append(
                f"{idx}. {title} - {price:,}Ä‘\n"
                f"   - Tá»“n kho: {'CÃ²n hÃ ng' if stock > 0 else 'Táº¡m háº¿t hÃ ng'}\n"
                f"   - LÃ½ do: {'; '.join(reasons)}"
            )
        dynamic = self._dynamic_context(snapshot)
        if dynamic:
            lines.append("\nNgá»¯ cáº£nh mua sáº¯m hiá»‡n táº¡i:")
            lines.append(dynamic)
        lines.append("\nNáº¿u báº¡n muá»‘n, mÃ¬nh cÃ³ thá»ƒ lá»c tiáº¿p theo ngÃ¢n sÃ¡ch hoáº·c chá»n ra 1 sáº£n pháº©m ná»•i báº­t nháº¥t trong nhÃ³m nÃ y.")
        return "\n".join(lines)

    def _format_availability_answer(
        self,
        user_name: str,
        product: dict[str, Any] | None,
        category_name: str | None,
        matched_products: list[dict[str, Any]],
    ) -> str:
        if product:
            title = product.get("title") or product.get("name") or "Sáº£n pháº©m"
            price = int(float(product.get("price", 0) or 0))
            stock = int(product.get("stock_quantity", 0) or 0)
            status = "CÃ²n hÃ ng" if stock > 0 else "Táº¡m háº¿t hÃ ng"
            return "\n".join(
                [
                    f"CÃ³, shop hiá»‡n cÃ³ {title}.",
                    f"Danh má»¥c: {category_name or 'KhÃ¡c'}",
                    f"GiÃ¡ hiá»‡n táº¡i: {price:,}Ä‘",
                    f"TÃ¬nh tráº¡ng: {status}",
                    "Náº¿u báº¡n muá»‘n, mÃ¬nh cÃ³ thá»ƒ gá»£i Ã½ thÃªm cÃ¡c lá»±a chá»n cÃ¹ng nhÃ³m hoáº·c cÃ¹ng táº§m giÃ¡.",
                ]
            )

        if category_name and matched_products:
            category_label = self._category_label(category_name)
            lines = [
                f"CÃ³, shop hiá»‡n cÃ³ bÃ¡n {category_label}.",
                "",
                f"Má»™t vÃ i sáº£n pháº©m thuá»™c {category_label}:",
            ]
            for idx, item in enumerate(matched_products[:3], start=1):
                title = item.get("title") or item.get("name") or "Sáº£n pháº©m"
                price = int(float(item.get("price", 0) or 0))
                stock = int(item.get("stock_quantity", 0) or 0)
                lines.append(f"{idx}. {title} - {price:,}Ä‘ - {'CÃ²n hÃ ng' if stock > 0 else 'Táº¡m háº¿t hÃ ng'}")
            lines.append("")
            lines.append(f"Náº¿u báº¡n muá»‘n, mÃ¬nh cÃ³ thá»ƒ lá»c tiáº¿p theo táº§m giÃ¡ hoáº·c chá»n máº«u phÃ¹ há»£p nháº¥t trong pháº§n {category_label}.")
            return "\n".join(lines)

        return (
            f"Hiá»‡n mÃ¬nh chÆ°a tháº¥y sáº£n pháº©m phÃ¹ há»£p Ä‘Ãºng vá»›i yÃªu cáº§u cá»§a {user_name}. "
            "Báº¡n thá»­ gá»­i tÃªn sáº£n pháº©m hoáº·c nhÃ³m cá»¥ thá»ƒ hÆ¡n Ä‘á»ƒ mÃ¬nh kiá»ƒm tra láº¡i."
        )

    def answer(self, customer_id: int, question: str, user_name: str = "KhÃ¡ch hÃ ng") -> dict[str, Any]:
        snapshot = self.services.get_user_snapshot(customer_id)
        base_behavior = self.behavior_model.predict(snapshot.get("feature_values", {}))
        sequence_behavior = self.sequence_behavior_model.predict(snapshot)
        behavior = sequence_behavior if sequence_behavior.used_sequence_model else base_behavior
        snapshot["behavior"] = behavior
        snapshot["behavior_fallback"] = base_behavior

        intent = classify_intent(question)
        kb_hits = self.kb.search(question, top_k=4)
        categories = snapshot.get("categories", [])
        products = snapshot.get("products", [])
        strict_categories = detect_categories_strict(question)
        explicit_product, is_exact = find_explicit_product(question, products, target_categories=strict_categories)
        preferred = snapshot.get("preferred_categories", [])
        greeting = f"MÃ¬nh Ä‘ang tÆ° váº¥n cho {user_name}."
        category_lookup = {item.get("id"): item.get("name") for item in categories}
        
        try:
            self.graph.sync_user_knowledge_graph(customer_id, snapshot)
        except Exception as e:
            print(f"Error syncing user graph: {e}")
            
        graph_context = self.graph.get_context(customer_id, question, top_k=6)
        top_products = self._score_products(products, categories, snapshot, question, graph_context=graph_context)[:3]

        if intent == "availability_query":
            if explicit_product:
                category_name = self._category_name(explicit_product, category_lookup)
                
                if is_exact:
                    ans = self._format_availability_answer(user_name, explicit_product, category_name, [explicit_product])
                else:
                    title = explicit_product.get("title") or explicit_product.get("name") or "Sáº£n pháº©m"
                    price = int(float(explicit_product.get("price", 0) or 0))
                    ans = (f"Hiá»‡n mÃ¬nh khÃ´ng tÃ¬m tháº¥y sáº£n pháº©m chÃ­nh xÃ¡c nhÆ° báº¡n yÃªu cáº§u, nhÆ°ng shop cÃ³ {title} "
                           f"vá»›i giÃ¡ {price:,}Ä‘. Báº¡n xem thá»­ cÃ³ phÃ¹ há»£p khÃ´ng nhÃ©.")

                return {
                    "answer": ans,
                    "top_products": [explicit_product],
                    "kb_hits": [hit.__dict__ for hit in kb_hits],
                    "behavior": behavior.__dict__,
                    "graph_context": graph_context,
                }

            if strict_categories:
                requested_category = strict_categories[0]
                matched_products = [
                    product
                    for product in products
                    if self._category_name(product, category_lookup) == requested_category
                ]
                # Kiá»ƒm tra xem cÃ³ sáº£n pháº©m nÃ o khá»›p tá»« khoÃ¡ cá»¥ thá»ƒ (vd: "balo") khÃ´ng
                q_norm = _searchable_text(question)
                keyword_matched = [
                    p for p in matched_products
                    if any(token in _searchable_text(str(p.get("title") or p.get("name") or ""))
                           for token in q_norm.split() if len(token) >= 4)
                ]
                if keyword_matched:
                    matched_products = keyword_matched
                elif not matched_products:
                    return {
                        "answer": f"Ráº¥t tiáº¿c, shop hiá»‡n chÆ°a cÃ³ sáº£n pháº©m {requested_category.lower()} mÃ  báº¡n tÃ¬m. Báº¡n thá»­ há»i mÃ¬nh vá» danh má»¥c khÃ¡c nhÆ° Ä‘iá»‡n thoáº¡i, sÃ¡ch, Ä‘á»“ gia dá»¥ng nhÃ©.",
                        "top_products": [],
                        "kb_hits": [hit.__dict__ for hit in kb_hits],
                        "behavior": behavior.__dict__,
                        "graph_context": graph_context,
                    }
                matched_products.sort(
                    key=lambda product: (
                        int(product.get("stock_quantity", 0) or 0) <= 0,
                        float(product.get("price", 0) or 0),
                    )
                )
                return {
                    "answer": self._format_availability_answer(user_name, None, requested_category, matched_products),
                    "top_products": matched_products[:3],
                    "kb_hits": [hit.__dict__ for hit in kb_hits],
                    "behavior": behavior.__dict__,
                    "graph_context": graph_context,
                }

            return {
                "answer": (
                    f"MÃ¬nh chÆ°a tÃ¬m tháº¥y sáº£n pháº©m báº¡n cáº§n. Shop cÃ³ sÃ¡ch, Ä‘iá»‡n thoáº¡i, laptop, phá»¥ kiá»‡n sá»‘, "
                    "thá»i trang, Ä‘á»“ gia dá»¥ng, lÃ m Ä‘áº¹p, sá»©c khá»e... Báº¡n thá»­ gá»­i tÃªn cá»¥ thá»ƒ hÆ¡n nhÃ©."
                ),
                "top_products": [],
                "kb_hits": [hit.__dict__ for hit in kb_hits],
                "behavior": behavior.__dict__,
                "graph_context": graph_context,
            }

        if intent == "purchase_request" and explicit_product:
            category_name = self._category_name(explicit_product, category_lookup)
            return {
                "answer": self._format_purchase_answer(user_name, explicit_product, category_name, behavior, snapshot),
                "top_products": [explicit_product],
                "kb_hits": [hit.__dict__ for hit in kb_hits],
                "behavior": behavior.__dict__,
                "graph_context": graph_context,
            }

        if intent == "purchase_request" and strict_categories:
            requested_category = strict_categories[0]
            category_ranked = self._score_products(
                products,
                categories,
                snapshot,
                question,
                forced_categories=[requested_category],
                graph_context=graph_context,
            )[:3]
            if category_ranked:
                return {
                    "answer": self._format_category_purchase_answer(user_name, requested_category, category_ranked, snapshot),
                    "top_products": [item["product"] for item in category_ranked],
                    "kb_hits": [hit.__dict__ for hit in kb_hits],
                    "behavior": behavior.__dict__,
                    "graph_context": graph_context,
                }

        if intent == "purchase_request":
            intent = "product_recommendation"

        if intent == "product_recommendation":
            # Æ¯u tiÃªn: náº¿u tÃ¬m Ä‘Æ°á»£c sáº£n pháº©m
            if explicit_product:
                category_name = self._category_name(explicit_product, category_lookup)
                price = int(float(explicit_product.get("price", 0) or 0))
                stock = int(explicit_product.get("stock_quantity", 0) or 0)
                title = explicit_product.get("title") or explicit_product.get("name") or "Sáº£n pháº©m"
                desc = explicit_product.get("description") or ""
                
                if is_exact:
                    lines = [
                        greeting, "",
                        f"{title} - {price:,}Ä‘",
                        f"Danh má»¥c: {category_name}",
                        f"TÃ¬nh tráº¡ng: {'CÃ²n hÃ ng' if stock > 0 else 'Táº¡m háº¿t hÃ ng'}",
                    ]
                else:
                    lines = [
                        greeting, "",
                        f"MÃ¬nh khÃ´ng tÃ¬m tháº¥y chÃ­nh xÃ¡c sáº£n pháº©m Ä‘Ã³, nhÆ°ng báº¡n xem qua {title} ({price:,}Ä‘) thuá»™c nhÃ³m {category_name} nhÃ©.",
                        f"TÃ¬nh tráº¡ng: {'CÃ²n hÃ ng' if stock > 0 else 'Táº¡m háº¿t hÃ ng'}",
                    ]
                
                if desc:
                    lines.append(f"MÃ´ táº£: {desc}")
                lines.append("Báº¡n muá»‘n mÃ¬nh thÃªm vÃ o giá» hÃ ng hoáº·c tÃ¬m thÃªm sáº£n pháº©m cÃ¹ng nhÃ³m khÃ´ng?")
                return {
                    "answer": "\n".join(lines),
                    "top_products": [explicit_product],
                    "kb_hits": [hit.__dict__ for hit in kb_hits],
                    "behavior": behavior.__dict__,
                    "graph_context": graph_context,
                }
            scoped_products = top_products
            if strict_categories:
                scoped_products = self._score_products(
                    products,
                    categories,
                    snapshot,
                    question,
                    forced_categories=strict_categories,
                    graph_context=graph_context,
                )[:3]

            if scoped_products:
                lines = [greeting, "", "Gá»£i Ã½ sáº£n pháº©m phÃ¹ há»£p nháº¥t:"]
                for idx, item in enumerate(scoped_products, start=1):
                    product = item["product"]
                    title = product.get("title") or product.get("name") or "Sáº£n pháº©m"
                    reasons = item["reasons"][:2] or ["phÃ¹ há»£p nhu cáº§u mua sáº¯m hiá»‡n táº¡i"]
                    lines.append(
                        f"{idx}. {title} - {int(float(product.get('price', 0) or 0)):,}Ä‘\n"
                        f"   - Danh má»¥c: {item['category_name']}.\n"
                        f"   - LÃ½ do: {'; '.join(reasons)}.\n"
                        f"   - MÃ´ táº£ ngáº¯n: {product.get('description') or 'Sáº£n pháº©m Ä‘ang cÃ³ trong catalog hiá»‡n táº¡i.'}"
                    )
                if preferred:
                    lines.append(f"\nMÃ¬nh Æ°u tiÃªn cÃ¡c danh má»¥c báº¡n quan tÃ¢m gáº§n Ä‘Ã¢y: {', '.join(preferred[:3])}.")
                if graph_context.get("preferred_categories"):
                    lines.append(f"\nGraph Ä‘ang cho tháº¥y báº¡n quan tÃ¢m nhiá»u Ä‘áº¿n: {', '.join(graph_context['preferred_categories'][:3])}.")
                if graph_context.get("preferred_brands"):
                    lines.append(f"Brand báº¡n tÆ°Æ¡ng tÃ¡c nhiá»u: {', '.join(graph_context['preferred_brands'][:3])}.")
                if graph_context.get("active_promotions"):
                    lines.append(f"Khuyáº¿n mÃ£i Ä‘ang cháº¡m tá»›i cÃ¡c sáº£n pháº©m báº¡n quan tÃ¢m: {', '.join(graph_context['active_promotions'][:2])}.")
                if behavior.next_best_action == "push_coupon":
                    dynamic = self._dynamic_context(snapshot)
                    if dynamic:
                        lines.append(f"\nNáº¿u báº¡n muá»‘n chá»‘t Ä‘Æ¡n sá»›m, hiá»‡n cÃ³ vÃ i Æ°u Ä‘Ã£i cÃ³ thá»ƒ táº­n dá»¥ng:\n{dynamic}")
                return {
                    "answer": "\n".join(lines),
                    "top_products": [item["product"] for item in scoped_products],
                    "kb_hits": [hit.__dict__ for hit in kb_hits],
                    "behavior": behavior.__dict__,
                    "graph_context": graph_context,
                }
            return {
                "answer": greeting + "\n\nHiá»‡n catalog chÆ°a cÃ³ sáº£n pháº©m khá»›p Ä‘Ãºng ngÃ¢n sÃ¡ch hoáº·c danh má»¥c báº¡n há»i.",
                "top_products": [],
                "kb_hits": [hit.__dict__ for hit in kb_hits],
                "behavior": behavior.__dict__,
                "graph_context": graph_context,
            }

        if intent == "policy":
            lines = [greeting, ""]
            if kb_hits:
                best_hit = kb_hits[0]
                lines.append(f"Theo '{best_hit.title}':")
                lines.append(f"{best_hit.content}")
                lines.append("")
            else:
                lines.append("MÃ¬nh tÃ³m táº¯t ngáº¯n gá»n nhÆ° sau:")

            dynamic = self._dynamic_context(snapshot)
            if dynamic and not kb_hits:
                lines.append("Dá»±a trÃªn tráº¡ng thÃ¡i hiá»‡n táº¡i cá»§a tÃ i khoáº£n vÃ  giá» hÃ ng:")
                lines.append(dynamic)
            elif not kb_hits:
                lines.append("MÃ¬nh Ä‘ang tráº£ lá»i dá»±a trÃªn chÃ­nh sÃ¡ch vÃ  dá»¯ liá»‡u há»‡ thá»‘ng hiá»‡n táº¡i.")
            return {
                "answer": "\n".join(lines),
                "top_products": [],
                "kb_hits": [hit.__dict__ for hit in kb_hits],
                "behavior": behavior.__dict__,
                "graph_context": graph_context,
            }

        if intent == "catalog_list":
            cats_in_catalog = sorted(set(self._category_name(p, category_lookup) for p in products if self._category_name(p, category_lookup) != "KhÃ¡c"))
            return {
                "answer": f"{greeting}\n\nShop hiá»‡n Ä‘ang bÃ¡n cÃ¡c nhÃ³m hÃ ng sau:\n" + "\n".join(f"â€¢ {c}" for c in cats_in_catalog),
                "top_products": [item["product"] for item in top_products],
                "kb_hits": [hit.__dict__ for hit in kb_hits],
                "behavior": behavior.__dict__,
                "graph_context": graph_context,
            }

        lines = [
            greeting,
            "",
            "MÃ¬nh cÃ³ thá»ƒ gá»£i Ã½ sáº£n pháº©m theo ngÃ¢n sÃ¡ch hoáº·c danh má»¥c, Ä‘á»“ng thá»i há»— trá»£ cÃ¡c cÃ¢u há»i vá» coupon, thÃ nh viÃªn, váº­n chuyá»ƒn, giá» hÃ ng, thanh toÃ¡n vÃ  Ä‘á»•i tráº£.",
        ]
        if preferred:
            lines.append(f"Gáº§n Ä‘Ã¢y báº¡n Ä‘ang quan tÃ¢m nhiá»u Ä‘áº¿n: {', '.join(preferred[:3])}.")
        return {
            "answer": "\n".join(lines),
            "top_products": [item["product"] for item in top_products],
            "kb_hits": [hit.__dict__ for hit in kb_hits],
            "behavior": behavior.__dict__,
            "graph_context": graph_context,
        }

    def recommend(self, customer_id: int, user_name: str = "KhÃ¡ch hÃ ng", limit: int = 6) -> dict[str, Any]:
        snapshot = self.services.get_user_snapshot(customer_id)
        base_behavior = self.behavior_model.predict(snapshot.get("feature_values", {}))
        sequence_behavior = self.sequence_behavior_model.predict(snapshot)
        behavior = sequence_behavior if sequence_behavior.used_sequence_model else base_behavior
        snapshot["behavior"] = behavior
        snapshot["behavior_fallback"] = base_behavior

        recent_search_terms = snapshot.get("recent_search_terms", [])
        preferred_categories = snapshot.get("preferred_categories", [])
        synthetic_question = " ".join(recent_search_terms[-3:] + preferred_categories[:2]).strip() or "goi y san pham phu hop"
        
        try:
            self.graph.sync_user_knowledge_graph(customer_id, snapshot)
        except Exception as e:
            print(f"Error syncing user graph: {e}")
            
        graph_context = self.graph.get_context(customer_id, synthetic_question, top_k=max(limit, 6))
        ranked = self._score_products(
            snapshot.get("products", []),
            snapshot.get("categories", []),
            snapshot,
            synthetic_question,
            graph_context=graph_context,
        )
        picks = ranked[:limit]

        reasons: list[str] = []
        if recent_search_terms:
            reasons.append(f"dá»±a trÃªn tÃ¬m kiáº¿m gáº§n Ä‘Ã¢y: {', '.join(recent_search_terms[-3:])}")
        if preferred_categories:
            reasons.append(f"Æ°u tiÃªn danh má»¥c: {', '.join(preferred_categories[:3])}")
        if graph_context.get("preferred_categories"):
            reasons.append(f"graph quan tÃ¢m máº¡nh: {', '.join(graph_context['preferred_categories'][:3])}")
        if not reasons:
            reasons.append("dá»±a trÃªn hÃ nh vi mua sáº¯m gáº§n Ä‘Ã¢y")

        return {
            "title": f"Gá»£i Ã½ cho {user_name}",
            "summary": "; ".join(reasons),
            "products": [item["product"] for item in picks],
            "behavior": behavior.__dict__,
            "graph_context": graph_context,
        }

