from django.shortcuts import render
from xadmin.views.base import BaseAdminView, ModelAdminView, filter_hook, csrf_protect_m
import collections
from xadmin.views import Dashboard


# Create your views here.
class MyDashboard(Dashboard, BaseAdminView):
    template_name = 'dashboard/my_dashboard.html'

    @filter_hook
    def get_context(self):
        context = Dashboard.get_context(self)
        return context

    def get(self, request, *args, **kwargs):
        return self.template_response(self.template_name, self.get_context())
