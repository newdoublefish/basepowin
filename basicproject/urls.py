"""basicproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from basicproject import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
import xadmin

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    path("api-docs/", include_docs_urls("API文档")),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^swagger/', schema_view, name="swagger"),
    url(r'^api/', include('procedure.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
