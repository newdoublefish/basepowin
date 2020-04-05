from django.conf.urls import url
from rest_framework import routers
from .views import DepartmentViewSet, RoleViewSet, UserProfileViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register("department", DepartmentViewSet)
router.register("role", RoleViewSet)
router.register("user", UserProfileViewSet)

urlpatterns = [
    url(r'user/login/', CustomAuthToken.as_view()),
]

urlpatterns += router.urls
