from django.urls import path
from .views import PaymentStatusView, OnlinePaymentView, RefundView, TransactionListView

urlpatterns = [
    path('<int:order_id>', PaymentStatusView.as_view()),           # GET  /payments/<order_id>
    path('<int:order_id>/process', OnlinePaymentView.as_view()),   # POST /payments/<order_id>/process
    path('<int:order_id>/refund', RefundView.as_view()),           # POST /payments/<order_id>/refund
    path('refunds/<int:refund_id>', RefundView.as_view()),         # PATCH /payments/refunds/<id>
    path('transactions', TransactionListView.as_view()),            # GET  /payments/transactions
]
