import xadmin
from .models import Version


class VersionAdmin(object):
    list_display = ('terminal_type', 'version', 'is_valid', 'app_url')
    model_icon = 'fa fa-bookmark'


xadmin.site.register(Version, VersionAdmin)
