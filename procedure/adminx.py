import xadmin
from .models import Mop, Procedure, Receipt, Task

xadmin.site.register(Mop)
xadmin.site.register(Procedure)
xadmin.site.register(Receipt)
xadmin.site.register(Task)
