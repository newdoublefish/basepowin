import xadmin
from .models import Role, UserProfile, Department
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AdminPasswordChangeForm, PasswordChangeForm)
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper


class UserProfilesAdmin(object):
    change_user_password_template = None
    list_display = ('username', 'dept', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    exclude = ('user_permissions', 'groups')

    # def get_field_attrs(self, db_field, **kwargs):
    #     attrs = super(UserProfilesAdmin, self).get_field_attrs(db_field, **kwargs)
    #     if db_field.name == 'user_permissions':
    #         attrs['form_class'] = PermissionModelMultipleChoiceField
    #     return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserProfilesAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset('Personal info',
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    # Fieldset('Permissions',
                    #          'groups', 'user_permissions'
                    #          ),
                    Fieldset('Important dates',
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset('Status',
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserProfilesAdmin, self).get_form_layout()


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

