import xadmin
from .models import Role, UserProfile, Department


class UserProfilesAdmin(object):
    list_display = ['id', 'username', 'mobile', 'email', 'date_joined', 'modifyCode']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
    # style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}
    exclude = ('user_permissions', 'groups')
    # 多对多样式字段支持过滤
    filter_horizontal = ('role',)
    # 多对多穿梭框样式
    style_fields = {'role': 'm2m_transfer'}

    def modifyCode(self, obj):
        return """<a href="/xadmin/user/userprofile/%d/password/" target="_parent">%s</a>""" % (obj.id, '修改密码')

    modifyCode.short_description = "修改密码"
    modifyCode.allow_tags = True
    modifyCode.is_column = True

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.fields = ['username', 'mobile', 'is_staff']

        return super().get_model_form(**kwargs)


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
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfilesAdmin)

