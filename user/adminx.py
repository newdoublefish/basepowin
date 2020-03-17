import xadmin
from .models import Role, UserProfile


class UserProfilesAdmin(object):
    list_display = ('id', 'username', )


class RoleAdmin(object):
    list_display = ('id', 'name')


xadmin.site.register(Role, RoleAdmin)
# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfilesAdmin)
