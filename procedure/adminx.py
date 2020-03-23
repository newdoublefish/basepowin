import xadmin
from .models import Mop, Procedure, Receipt, Task


class MopAdmin(object):
    model_icon = 'fa fa-bars '
    list_display = ('manufacture_order_name', 'sell_order_name', 'part_no_name', 'quantity', 'status')


class ProcedureAdmin(object):
    model_icon = "fa fa-hand-o-right"


class ReceiptAdmin(object):
    model_icon = "fa fa-paperclip"


class TaskAdmin(object):
    model_icon = "fa fa-tasks"


xadmin.site.register(Mop, MopAdmin)
xadmin.site.register(Procedure, ProcedureAdmin)
xadmin.site.register(Receipt, ReceiptAdmin)
xadmin.site.register(Task, TaskAdmin)
