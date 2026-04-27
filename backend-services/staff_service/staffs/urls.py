from django.urls import path
from .views import (
    health, list_departments, create_department,
    list_members, create_member, get_member, deactivate_member, staff_metrics
)

urlpatterns = [
    path('health', health),
    path('departments', list_departments),
    path('departments/create', create_department),
    path('members', list_members),
    path('members/create', create_member),
    path('members/<int:staff_id>', get_member),
    path('members/<int:staff_id>/deactivate', deactivate_member),
    path('metrics', staff_metrics),
]
