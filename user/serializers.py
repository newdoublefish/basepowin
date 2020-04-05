from rest_framework import serializers
from .models import Department, Role, UserProfile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    dept_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'first_name', 'last_name', 'is_active', 'role', 'dept', 'is_staff', 'user_permissions',
            'dept_name', 'role_name')
        read_only = ('user_permissions',)

    def get_role_name(self, obj):
        if obj.role is not None:
            role_list = obj.role.all()
            role_name = ""
            for role in role_list:
                role_name = role_name + role.name + ";"
            return role_name

    def get_dept_name(self, obj):
        if obj.dept is not None:
            return obj.dept.name
