from django.contrib import admin
from .models import Version


class VersionAdmin(admin.ModelAdmin):
    list_display = ('terminal_type', 'version', 'is_valid', 'app_url')


# Register your models here.
admin.site.register(Version, VersionAdmin)
