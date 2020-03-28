import xadmin
from .models import Mop, Procedure, Receipt, Task
from xadmin.layout import Main, Side, Fieldset, Row, AppendedText


class MopAdmin(object):
    model_icon = 'fa fa-bars '
    list_display = ('manufacture_order_name', 'sell_order_name', 'part_no_name', 'quantity', 'status')
    search_fields = ('manufacture_order_name', 'sell_order_name', 'part_no_name',)
    list_filter = ('manufacture_order_name', 'sell_order_name', 'part_no_name', 'status',)


class ReceiptInline(object):
    # http://xadmin.readthedocs.io/en/docs-chinese/views_api.html?highlight=fieldsets
    model = Receipt
    extra = 0
    fk_name = 'deliver_procedure'
    form_layout = (
        Main(
            Row('deliver_type', 'deliver_procedure', 'receiver_procedure', 'quantity', 'deliver', 'receiver', 'status'),
        ),
    )
    exclude = []


class ProcedureAdmin(object):
    list_display = (
        'name', 'mop', 'part_no_name', 'dept', 'quantity', 'received_quantity', 'delivered_quantity', 'remake_quantity',
        'status')
    model_icon = "fa fa-hand-o-right"
    list_filter = ('name', 'mop', 'part_no_name', 'dept', 'status')
    search_fields = ('name', 'part_no_name', 'mop_name')
    # inlines = [ReceiptInline, ]


class ReceiptAdmin(object):
    model_icon = "fa fa-paperclip"
    list_filter = ('status',)
    list_display = (
        'deliver_type', 'deliver_procedure', 'receiver_procedure', 'quantity', 'deliver', 'receiver', 'status')


class TaskAdmin(object):
    model_icon = "fa fa-tasks"
    list_display = (
        'name', 'sub_procedure', 'procedure', 'quantity', 'weight', 'user', 'started_at',
        'stopped_at')


xadmin.site.register(Mop, MopAdmin)
xadmin.site.register(Procedure, ProcedureAdmin)
xadmin.site.register(Receipt, ReceiptAdmin)
xadmin.site.register(Task, TaskAdmin)
