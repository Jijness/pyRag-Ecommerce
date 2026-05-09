from django.urls import path, re_path
from gateway.views import gateway_proxy, health_check

urlpatterns = [
    path('health', health_check),
    re_path(r'^(?P<path>.*)$', gateway_proxy),
]
