from django.apps import AppConfig
import os

class CoreAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_ai'

    def ready(self):
        # Không tự động chạy logic nặng trong lúc migrate
        if os.environ.get('RUN_MAIN') or os.environ.get('UVICORN_RELOAD_FLAG'):
            from .graph_store import GraphKBStore
            from .kb_store import KBStore
            from .behavior_model import BehaviorModel
            from django.conf import settings

            print("Initializing Core AI components...")
            # Init components and bind to AppConfig for global access
            self.graph_store = GraphKBStore(settings.BASE_DIR)
            self.kb_store = KBStore(settings.BASE_DIR)
            self.behavior_model = BehaviorModel(settings.AI_MODELS_DIR)

            try:
                self.behavior_model.ensure_ready()
                self.kb_store.ensure_ready()
                self.graph_store.ensure_ready()
                # Cần sync_catalog, sync_marketing không?
                # Khuyến cáo nên dùng management command để sync thay vì sync lúc khởi động app
            except Exception as e:
                print(f"Failed to initialize AI components: {e}")
