from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.apps import apps
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

_metrics = {"chat_requests": 0, "started_at": datetime.utcnow().isoformat()}

def get_advisor():
    from .advisor import MarketplaceAdvisor
    return MarketplaceAdvisor(settings.BASE_DIR)

class MetricsView(APIView):
    def get(self, request):
        return Response(_metrics)

class ChatAskView(APIView):
    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response({"error": "Missing question"}, status=status.HTTP_400_BAD_REQUEST)
        
        customer_id = request.headers.get("X-Customer-Id")
        if not customer_id:
            return Response({"error": "Missing X-Customer-Id"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_name = request.headers.get("X-Customer-Name", "Khách hàng")
        _metrics["chat_requests"] += 1

        advisor = get_advisor()
        try:
            result = advisor.answer(customer_id=int(customer_id), question=question, user_name=user_name)
            return Response(result)
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecommendationsView(APIView):
    def get(self, request):
        customer_id = request.headers.get("X-Customer-Id")
        if not customer_id:
            return Response({"error": "Missing X-Customer-Id"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_name = request.headers.get("X-Customer-Name", "Khách hàng")
        limit = int(request.query_params.get("limit", 6))
        
        advisor = get_advisor()
        try:
            result = advisor.recommend(customer_id=int(customer_id), user_name=user_name, limit=limit)
            return Response(result)
        except Exception as e:
            logger.error(f"Recommend error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DebugProfileView(APIView):
    def get(self, request):
        customer_id = request.headers.get("X-Customer-Id")
        if not customer_id:
            return Response({"error": "Missing X-Customer-Id"}, status=status.HTTP_401_UNAUTHORIZED)
        
        advisor = get_advisor()
        try:
            snapshot = advisor.services.get_user_snapshot(int(customer_id))
            fallback_behavior = advisor.behavior_model.predict(snapshot.get("feature_values", {}))
            sequence_behavior = advisor.sequence_behavior_model.predict(snapshot)
            return Response({
                "snapshot": snapshot,
                "behavior": fallback_behavior.__dict__,
                "sequence_behavior": sequence_behavior.__dict__
            })
        except Exception as e:
            logger.error(f"Profile debug error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SyncProductView(APIView):
    def post(self, request):
        data = request.data
        if "id" not in data or "title" not in data:
            return Response({"error": "Missing id or title"}, status=status.HTTP_400_BAD_REQUEST)
        
        advisor = get_advisor()
        try:
            advisor.graph.upsert_product(data)
            return Response({"status": "ok", "product_id": data["id"], "message": "Graph synced successfully"})
        except Exception as e:
            logger.error(f"Product sync error: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
