from rest_framework import routers
from .views import DepartmentViewSet, RoleViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register("department", DepartmentViewSet)
router.register("role", RoleViewSet)
router.register("user", UserProfileViewSet)

urlpatterns = [
    # url(r'^flow/check/$', FlowCheck.as_view())
]

urlpatterns += router.urls
