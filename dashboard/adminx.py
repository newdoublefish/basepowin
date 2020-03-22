import xadmin
from .views import MyDashboard

xadmin.site.register_view(r'dashboard/$', MyDashboard, name="dashboard")