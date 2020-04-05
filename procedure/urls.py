from rest_framework import routers
from django.conf.urls import url
from .views import MopViewSet, ProcedureViewSet, ReceiptViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register("procedure/mop", MopViewSet)
router.register("procedure/procedure", ProcedureViewSet)
router.register("procedure/receipt", ReceiptViewSet)
router.register("procedure/task", TaskViewSet)

urlpatterns = [
    # url(r'^flow/check/$', FlowCheck.as_view())
]

urlpatterns += router.urls
