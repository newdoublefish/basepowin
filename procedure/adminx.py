import xadmin
from .models import Mop, Procedure, Receipt, Task


class MopAdmin(object):
    model_icon = 'fa fa-bars '
    list_display = ('manufacture_order_name', 'sell_order_name', 'part_no_name', 'quantity', 'status')
    search_fields = ('manufacture_order_name', 'sell_order_name', 'part_no_name',)
    list_filter = ('manufacture_order_name', 'sell_order_name', 'part_no_name', 'status',)


class ProcedureAdmin(object):
    list_display = ('name', 'mop', 'part_no_name', 'dept', 'quantity', 'status')
    model_icon = "fa fa-hand-o-right"
    list_filter = ('name', 'mop', 'part_no_name', 'dept', 'status')
    search_fields = ('name', 'part_no_name', 'mop_name')


class ReceiptAdmin(object):
    model_icon = "fa fa-paperclip"
    list_display = (
        'deliver_type', 'deliver_procedure', 'receiver_procedure', 'quantity', 'deliver', 'receiver', 'status')


class TaskAdmin(object):
    model_icon = "fa fa-tasks"


xadmin.site.register(Mop, MopAdmin)
xadmin.site.register(Procedure, ProcedureAdmin)
xadmin.site.register(Receipt, ReceiptAdmin)
xadmin.site.register(Task, TaskAdmin)
