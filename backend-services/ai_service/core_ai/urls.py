from django.urls import path
from .views import MetricsView, ChatAskView, RecommendationsView, DebugProfileView, SyncProductView

urlpatterns = [
    path('metrics', MetricsView.as_view(), name='metrics'),
    path('chat/ask', ChatAskView.as_view(), name='chat_ask'),
    path('recommendations', RecommendationsView.as_view(), name='recommendations'),
    path('debug/profile', DebugProfileView.as_view(), name='debug_profile'),
    path('sync-product', SyncProductView.as_view(), name='sync_product'),
]
