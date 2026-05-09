from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error

from .deep_models import DeepClassifierV2, DeepRegressorV2

FEATURES = [
    "search_count", "view_count", "wishlist_count", "cart_item_count",
    "order_count", "avg_order_value", "total_spent", "promo_keyword_count",
    "membership_points", "preferred_genre_count",
]
PERSONAS = ["new_explorer", "category_browser", "deal_hunter", "loyal_member", "high_intent_buyer"]
PRICE_LEVELS = ["low", "medium", "high"]
ACTIONS = ["recommend_entry_products", "push_coupon", "bundle_related_products", "upsell_membership", "reengage_catalog"]
MODEL_KIND = "deep_adam_v2"

@dataclass
class BehaviorOutputs:
    persona: str
    price_sensitivity: str
    next_best_action: str
    purchase_intent: float

class BehaviorModel:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.model_dir = self.base_dir / "models"
        self.data_dir = self.base_dir / "data"
        self.plots_dir = self.base_dir / "plots"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        self.bundle_path = self.model_dir / "behavior_bundle_v2.joblib"
        self.bundle: dict[str, Any] | None = None

    def ensure_ready(self) -> None:
        if self.bundle is not None:
            return
        if self.bundle_path.exists():
            loaded = joblib.load(self.bundle_path)
            if isinstance(loaded, dict) and loaded.get("model_kind") == MODEL_KIND:
                self.bundle = loaded
                return
        self.train_and_save()

    def _sample_dataset_1_normal(self, rng: np.random.Generator, size: int) -> list:
        """Tập 1: Người dùng mua sắm ngẫu nhiên, phổ thông"""
        rows = []
        for _ in range(size):
            search = int(rng.integers(0, 15))
            views = int(rng.integers(search, search + 15))
            wishlist = int(rng.integers(0, 5))
            cart = int(rng.integers(0, 3))
            orders = int(rng.integers(0, 8))
            avg_value = float(rng.normal(120000, 30000))
            total_spent = float(avg_value * orders)
            promo = int(rng.integers(0, 3))
            points = int(total_spent // 10000)
            pref_categories = int(rng.integers(1, 4))
            rows.append([search, views, wishlist, cart, orders, max(10000, avg_value), total_spent, promo, points, pref_categories])
        return rows

    def _sample_dataset_2_promo(self, rng: np.random.Generator, size: int) -> list:
        """Tập 2: Nhóm chuyên tìm khuyến mãi (deal hunter)"""
        rows = []
        for _ in range(size):
            search = int(rng.integers(5, 25))
            views = int(rng.integers(10, 40))
            wishlist = int(rng.integers(2, 10))
            cart = int(rng.integers(1, 5))
            orders = int(rng.integers(0, 4))
            avg_value = float(rng.normal(80000, 20000))
            total_spent = float(avg_value * orders)
            promo = int(rng.integers(4, 15))
            points = int(total_spent // 10000)
            pref_categories = int(rng.integers(2, 6))
            rows.append([search, views, wishlist, cart, orders, max(10000, avg_value), total_spent, promo, points, pref_categories])
        return rows

    def _sample_dataset_3_high_intent(self, rng: np.random.Generator, size: int) -> list:
        """Tập 3: Khách VIP, chốt đơn nhanh, giá trị lớn (loyal, high intent)"""
        rows = []
        for _ in range(size):
            search = int(rng.integers(0, 5))
            views = int(rng.integers(2, 8))
            wishlist = int(rng.integers(0, 2))
            cart = int(rng.integers(1, 4))
            orders = int(rng.integers(5, 20))
            avg_value = float(rng.normal(500000, 150000))
            total_spent = float(avg_value * orders)
            promo = int(rng.integers(0, 2))
            points = int(total_spent // 10000 + 500)
            pref_categories = int(rng.integers(1, 3))
            rows.append([search, views, wishlist, cart, orders, max(100000, avg_value), total_spent, promo, points, pref_categories])
        return rows

    def _assign_labels(self, features: list[float], rng: np.random.Generator) -> tuple[str, str, str, float]:
        search, views, wishlist, cart, orders, avg_value, total_spent, promo, points, _ = features
        
        # Heuristic rules to assign ground truth for Synthetic dataset
        score = 0.2*search + 0.3*views + 0.5*wishlist + 1.0*cart + 0.8*orders - 0.2*promo
        intent = float(1 / (1 + np.exp(-(score - 4.0))))
        intent = float(np.clip(intent + rng.normal(0, 0.05), 0.01, 0.99))

        if orders == 0 and views <= 5:
            persona = "new_explorer"
        elif promo >= 4 or (orders > 0 and total_spent/orders < 100000):
            persona = "deal_hunter"
        elif orders >= 8 or total_spent > 2000000:
            persona = "loyal_member"
        elif cart >= 1 or intent > 0.7:
            persona = "high_intent_buyer"
        else:
            persona = "category_browser"

        if promo >= 4 or avg_value < 100000:
            price = "low"
        elif avg_value < 350000:
            price = "medium"
        else:
            price = "high"

        if persona == "deal_hunter":
            action = "push_coupon"
        elif persona == "loyal_member" and points >= 1000:
            action = "upsell_membership"
        elif persona == "high_intent_buyer":
            action = "bundle_related_products"
        elif persona == "new_explorer":
            action = "recommend_entry_products"
        else:
            action = "reengage_catalog"

        return persona, price, action, intent

    def generate_datasets(self, size_per_dataset=1500, seed=42):
        rng = np.random.default_rng(seed)
        d1 = self._sample_dataset_1_normal(rng, size_per_dataset)
        d2 = self._sample_dataset_2_promo(rng, size_per_dataset)
        d3 = self._sample_dataset_3_high_intent(rng, size_per_dataset)
        
        datasets = []
        for idx, d in enumerate([d1, d2, d3], 1):
            labeled = []
            for feats in d:
                labels = self._assign_labels(feats, rng)
                labeled.append((feats, *labels))
            self._write_mock_csv(labeled, f"dataset_{idx}.csv")
            datasets.extend(labeled)
            
        rng.shuffle(datasets)
        return datasets

    def train_and_save(self) -> None:
        print("Generating 3 datasets...")
        datasets = self.generate_datasets(1500)
        
        x_train = np.array([row[0] for row in datasets], dtype=np.float64)
        y_persona = [row[1] for row in datasets]
        y_price = [row[2] for row in datasets]
        y_action = [row[3] for row in datasets]
        y_intent = np.array([row[4] for row in datasets], dtype=np.float64)

        # One-hot encoding
        persona_targets = np.eye(len(PERSONAS), dtype=np.float64)[[PERSONAS.index(label) for label in y_persona]]
        price_targets = np.eye(len(PRICE_LEVELS), dtype=np.float64)[[PRICE_LEVELS.index(label) for label in y_price]]
        action_targets = np.eye(len(ACTIONS), dtype=np.float64)[[ACTIONS.index(label) for label in y_action]]

        print("Training models with Adam Optimizer & L2 Regularization...")
        persona_model = DeepClassifierV2(len(FEATURES), len(PERSONAS), hidden_dims=(128, 64, 32), learning_rate=0.002, epochs=250, l2_lambda=0.001)
        price_model = DeepClassifierV2(len(FEATURES), len(PRICE_LEVELS), hidden_dims=(64, 32), learning_rate=0.002, epochs=200, l2_lambda=0.001)
        action_model = DeepClassifierV2(len(FEATURES), len(ACTIONS), hidden_dims=(128, 64, 32), learning_rate=0.002, epochs=250, l2_lambda=0.001)
        intent_model = DeepRegressorV2(len(FEATURES), hidden_dims=(64, 32), learning_rate=0.001, epochs=200, l2_lambda=0.001)

        persona_model.fit(x_train, persona_targets)
        price_model.fit(x_train, price_targets)
        action_model.fit(x_train, action_targets)
        intent_model.fit(x_train, y_intent)

        self.bundle = {
            "model_kind": MODEL_KIND,
            "persona_model": persona_model,
            "price_model": price_model,
            "action_model": action_model,
            "intent_model": intent_model,
            "features": FEATURES,
        }
        joblib.dump(self.bundle, self.bundle_path)
        print("Models saved successfully. Generating evaluation plots...")
        
        self._generate_plots(persona_model, action_model, x_train, y_persona, y_action, intent_model, y_intent)

    def _generate_plots(self, p_model, a_model, X, y_p, y_a, i_model, y_i):
        # 1. Loss & Accuracy Curve (Persona)
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(p_model.history['loss'], label='Loss')
        plt.title('Persona Model: Training Loss')
        plt.xlabel('Epochs')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(p_model.history['accuracy'], label='Accuracy', color='orange')
        plt.title('Persona Model: Training Accuracy')
        plt.xlabel('Epochs')
        plt.legend()
        plt.savefig(self.plots_dir / 'persona_training_curves.png')
        plt.close()

        # 2. Confusion Matrix (Action)
        preds = a_model.predict(X, ACTIONS)
        cm = confusion_matrix(y_a, preds, labels=ACTIONS)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=ACTIONS, yticklabels=ACTIONS)
        plt.title('Next Best Action: Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'action_confusion_matrix.png')
        plt.close()

        # 3. Intent MSE
        preds_i = i_model.predict(X)
        mse = mean_squared_error(y_i, preds_i)
        plt.figure(figsize=(8, 6))
        plt.scatter(y_i[:200], preds_i[:200], alpha=0.5)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.title(f'Purchase Intent: Actual vs Predicted (MSE: {mse:.4f})')
        plt.xlabel('Actual Intent')
        plt.ylabel('Predicted Intent')
        plt.savefig(self.plots_dir / 'intent_regression_fit.png')
        plt.close()

    def _write_mock_csv(self, rows: list, filename: str) -> None:
        filepath = self.data_dir / filename
        with filepath.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(FEATURES + ["persona", "price_sensitivity", "next_best_action", "purchase_intent"])
            for r in rows:
                writer.writerow(r[0] + [r[1], r[2], r[3], round(r[4], 4)])

    def predict(self, feature_values: dict[str, Any]) -> BehaviorOutputs:
        self.ensure_ready()
        x_pred = np.array([[float(feature_values.get(name, 0) or 0) for name in FEATURES]], dtype=np.float64)
        
        persona = self.bundle["persona_model"].predict(x_pred, PERSONAS)[0]
        price = self.bundle["price_model"].predict(x_pred, PRICE_LEVELS)[0]
        action = self.bundle["action_model"].predict(x_pred, ACTIONS)[0]
        intent = float(np.clip(self.bundle["intent_model"].predict(x_pred)[0], 0.01, 0.99))

        return BehaviorOutputs(persona=persona, price_sensitivity=price, next_best_action=action, purchase_intent=intent)
