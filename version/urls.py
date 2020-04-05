from rest_framework import routers

from .views import VersionViewSet

router = routers.DefaultRouter()
router.register("version", VersionViewSet)

urlpatterns = [

]

urlpatterns += router.urls