from __future__ import annotations

import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

ACTIONS = [
    "search",
    "view",
    "click",
    "add_to_cart",
    "wishlist",
    "coupon_view",
    "checkout",
    "purchase",
]
CATEGORIES = [
    "Sách",
    "Dụng cụ học tập",
    "Đồ chơi",
    "Gói quà",
    "Ba lô",
    "Bình nước",
    "Đồ điện tử học tập",
    "Mỹ thuật",
    "Đồ trang trí bàn học",
    "Đồ lưu niệm",
]
PERSONAS = ["new_explorer", "category_browser", "deal_hunter", "loyal_member", "high_intent_buyer"]
NEXT_ACTIONS = [
    "recommend_entry_products",
    "push_coupon",
    "bundle_related_products",
    "upsell_membership",
    "reengage_catalog",
]
PRICE_SENSITIVITY = ["low", "medium", "high"]


@dataclass
class PersonaRule:
    persona: str
    action_weights: dict[str, float]
    price_range: tuple[int, int]
    price_sensitivity: str
    next_best_action: str


RULES: dict[str, PersonaRule] = {
    "new_explorer": PersonaRule(
        persona="new_explorer",
        action_weights={"search": 0.28, "view": 0.24, "click": 0.16, "add_to_cart": 0.08, "wishlist": 0.1, "coupon_view": 0.06, "checkout": 0.04, "purchase": 0.04},
        price_range=(35000, 120000),
        price_sensitivity="high",
        next_best_action="recommend_entry_products",
    ),
    "category_browser": PersonaRule(
        persona="category_browser",
        action_weights={"search": 0.18, "view": 0.26, "click": 0.18, "add_to_cart": 0.08, "wishlist": 0.12, "coupon_view": 0.05, "checkout": 0.06, "purchase": 0.07},
        price_range=(50000, 180000),
        price_sensitivity="medium",
        next_best_action="reengage_catalog",
    ),
    "deal_hunter": PersonaRule(
        persona="deal_hunter",
        action_weights={"search": 0.2, "view": 0.18, "click": 0.12, "add_to_cart": 0.1, "wishlist": 0.09, "coupon_view": 0.2, "checkout": 0.07, "purchase": 0.04},
        price_range=(25000, 110000),
        price_sensitivity="high",
        next_best_action="push_coupon",
    ),
    "loyal_member": PersonaRule(
        persona="loyal_member",
        action_weights={"search": 0.08, "view": 0.16, "click": 0.14, "add_to_cart": 0.16, "wishlist": 0.08, "coupon_view": 0.06, "checkout": 0.16, "purchase": 0.16},
        price_range=(120000, 320000),
        price_sensitivity="low",
        next_best_action="upsell_membership",
    ),
    "high_intent_buyer": PersonaRule(
        persona="high_intent_buyer",
        action_weights={"search": 0.1, "view": 0.18, "click": 0.14, "add_to_cart": 0.2, "wishlist": 0.08, "coupon_view": 0.05, "checkout": 0.14, "purchase": 0.11},
        price_range=(90000, 260000),
        price_sensitivity="medium",
        next_best_action="bundle_related_products",
    ),
}


def weighted_choice(rng: random.Random, weights: dict[str, float]) -> str:
    actions = list(weights.keys())
    probs = list(weights.values())
    return rng.choices(actions, weights=probs, k=1)[0]


def build_dataset(out_path: Path, user_count: int = 500, seed: int = 42) -> dict[str, int]:
    rng = random.Random(seed)
    start = datetime(2026, 1, 1, 8, 0, 0)
    rows: list[dict[str, object]] = []
    persona_counts: defaultdict[str, int] = defaultdict(int)

    persona_distribution = [
        ("new_explorer", 0.2),
        ("category_browser", 0.24),
        ("deal_hunter", 0.2),
        ("loyal_member", 0.16),
        ("high_intent_buyer", 0.2),
    ]
    persona_labels = [name for name, _ in persona_distribution]
    persona_weights = [weight for _, weight in persona_distribution]

    for user_id in range(1, user_count + 1):
        persona = rng.choices(persona_labels, weights=persona_weights, k=1)[0]
        persona_counts[persona] += 1
        rule = RULES[persona]
        base_category = rng.choice(CATEGORIES)
        sequence_length = rng.randint(18, 42)
        event_time = start + timedelta(hours=rng.randint(0, 24 * 45))
        session_index = 1
        purchase_count = 0

        for step in range(sequence_length):
            action = weighted_choice(rng, rule.action_weights)
            if action in {"checkout", "purchase"} and step < 4:
                action = rng.choice(["search", "view", "click"])
            if action == "purchase":
                purchase_count += 1
            if action == "purchase" and purchase_count > 3:
                action = rng.choice(["view", "add_to_cart", "checkout"])

            category_name = base_category if rng.random() < 0.65 else rng.choice(CATEGORIES)
            price = rng.randint(*rule.price_range)
            quantity = 1 if action != "purchase" else rng.randint(1, 2)
            if action == "coupon_view":
                query = rng.choice(["voucher", "sale", "coupon học tập", "khuyến mãi"])
            elif action == "search":
                query = rng.choice([
                    f"{category_name.lower()} giá tốt",
                    f"{category_name.lower()} cho học sinh",
                    f"mua {category_name.lower()} online",
                    f"{category_name.lower()} dưới {price // 1000}k",
                ])
            else:
                query = ""

            rows.append(
                {
                    "user_id": user_id,
                    "session_id": f"S{user_id:03d}-{session_index:02d}",
                    "step": step + 1,
                    "timestamp": event_time.isoformat(),
                    "product_id": rng.randint(1000, 1300),
                    "category_name": category_name,
                    "action": action,
                    "price": price,
                    "quantity": quantity,
                    "query": query,
                    "persona_label": persona,
                    "next_best_action": rule.next_best_action,
                    "price_sensitivity": rule.price_sensitivity,
                }
            )
            event_time += timedelta(minutes=rng.randint(2, 45))
            if rng.random() < 0.12:
                session_index += 1
                event_time += timedelta(hours=rng.randint(4, 36))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "user_id",
                "session_id",
                "step",
                "timestamp",
                "product_id",
                "category_name",
                "action",
                "price",
                "quantity",
                "query",
                "persona_label",
                "next_best_action",
                "price_sensitivity",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    return dict(sorted(persona_counts.items()))


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "ai_chat_service" / "data" / "data_user500.csv"
    stats = build_dataset(output)
    print(f"Wrote {output}")
    print(stats)
