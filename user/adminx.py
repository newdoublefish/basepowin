import xadmin
from .models import Role, UserProfile, Department


class UserProfilesAdmin(object):
    list_display = ('id', 'username', )


class RoleAdmin(object):
    list_display = ('id', 'name')
    # 多对多样式字段支持过滤
    filter_horizontal = ('groups',)
    # 多对多穿梭框样式
    style_fields = {'groups': 'm2m_transfer'}


class DepartmentAdmin(object):
    list_display = ('id', 'name', 'parent')
    filter_horizontal = ('admins',)
    style_fields = {'admins': 'm2m_transfer'}


xadmin.site.register(Role, RoleAdmin)
xadmin.site.register(Department, DepartmentAdmin)
# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfilesAdmin)
