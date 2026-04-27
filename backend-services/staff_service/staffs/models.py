from django.db import models


class StaffDepartment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'staff_departments'


class StaffMember(models.Model):
    staff_id = models.IntegerField(unique=True)
    department = models.ForeignKey(StaffDepartment, null=True, blank=True, on_delete=models.SET_NULL, db_column='department_id')
    phone = models.CharField(max_length=20, blank=True, null=True)
    salary = models.IntegerField(null=True, blank=True)
    hire_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'staff_members'
