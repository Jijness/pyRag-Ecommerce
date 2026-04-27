from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import StaffDepartment, StaffMember


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffDepartment
        fields = '__all__'


class StaffMemberSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source='department.id', read_only=True, allow_null=True)

    class Meta:
        model = StaffMember
        fields = ['id', 'staff_id', 'department_id', 'phone', 'salary', 'hire_date', 'is_active']


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'staff_service', 'timestamp': datetime.utcnow().isoformat()})


@api_view(['GET'])
def list_departments(request):
    depts = StaffDepartment.objects.all()
    return Response(DepartmentSerializer(depts, many=True).data)


@api_view(['POST'])
def create_department(request):
    s = DepartmentSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    dept = s.save()
    return Response(DepartmentSerializer(dept).data, status=201)


@api_view(['GET'])
def list_members(request):
    members = StaffMember.objects.all()
    return Response(StaffMemberSerializer(members, many=True).data)


@api_view(['POST'])
def create_member(request):
    data = request.data
    staff_id = data.get('staff_id')
    if StaffMember.objects.filter(staff_id=staff_id).exists():
        return Response({'detail': 'Thành viên đã tồn tại'}, status=400)
    dept_id = data.get('department_id')
    dept = StaffDepartment.objects.filter(id=dept_id).first() if dept_id else None
    member = StaffMember.objects.create(
        staff_id=staff_id,
        department=dept,
        phone=data.get('phone'),
        salary=data.get('salary'),
        is_active=data.get('is_active', True)
    )
    return Response(StaffMemberSerializer(member).data, status=201)


@api_view(['GET'])
def get_member(request, staff_id):
    member = StaffMember.objects.filter(staff_id=staff_id).first()
    if not member:
        return Response({'detail': 'Không tìm thấy nhân viên'}, status=404)
    return Response(StaffMemberSerializer(member).data)


@api_view(['PATCH'])
def deactivate_member(request, staff_id):
    member = StaffMember.objects.filter(staff_id=staff_id).first()
    if not member:
        return Response({'detail': 'Không tìm thấy nhân viên'}, status=404)
    member.is_active = False
    member.save()
    return Response({'message': f'Đã vô hiệu hóa nhân viên {staff_id}'})


@api_view(['GET'])
def staff_metrics(request):
    total = StaffMember.objects.count()
    active = StaffMember.objects.filter(is_active=True).count()
    return Response({'service': 'staff_service', 'total_members': total, 'active_members': active})
