import xadmin
from .models import Role, UserProfile, Department, fill_user_permissions
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AdminPasswordChangeForm, PasswordChangeForm)
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper
from xadmin import views
from django import forms
from django.db import transaction


class UserProfilesAdmin(object):
    change_user_password_template = None
    list_display = ('username', 'dept', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer', 'role': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    exclude = ('user_permissions', 'groups')

    # def save_related(self):
    #     obj = self.new_obj
    #     super(UserProfilesAdmin, self).save_related()
    #     role_list = obj.role.all()
    #     user_permissions_set = {permissions for role in role_list for permissions in role.permissions.all()}
    #     obj.user_permissions.clear()
    #     obj.user_permissions.add(*user_permissions_set)
    #     obj.save()

    def save_models(self):
        try:
            obj = self.new_obj
            if self.new_obj.id is None:
                obj.save()
            fill_user_permissions(obj)
            # else:
            #     super(UserProfilesAdmin, self).save_models()
        except Exception as e:
            raise forms.ValidationError(str(e))
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
                    Fieldset('个人信息',
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    # Fieldset('Permissions',
                    #          'groups', 'user_permissions'
                    #          ),
                    Fieldset('时间信息',
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
    filter_horizontal = ('permissions',)
    # 多对多穿梭框样式
    style_fields = {'permissions': 'm2m_transfer'}
    model_icon = 'fa fa-credit-card'


class DepartmentAdmin(object):
    list_display = ('id', 'name', 'parent')
    filter_horizontal = ('admins',)
    style_fields = {'admins': 'm2m_transfer'}
    model_icon = 'fa fa-group '


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "MCMC"  # 设置站点标题
    site_footer = "copyright mcmc 2020"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的
    # 设置models的全局图标, UserProfile, Sports 为表名
    global_search_models = [UserProfile, ]
    global_models_icon = {
        UserProfile: "glyphicon glyphicon-user", }


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Role, RoleAdmin)
xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfilesAdmin)
