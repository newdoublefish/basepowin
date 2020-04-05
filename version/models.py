from django.db import models


class Version(models.Model):
    TERMINAL_TYPE = (
        (0, u'PC'),
        (1, u"ANDROID"),
        (2, u"IOS"),
    )

    version = models.CharField(u'版本', max_length=20, blank=True, null=True)
    app_url = models.CharField(u'链接地址', max_length=200, blank=True, null=True)
    is_valid = models.BooleanField(u'有效', default=True)
    terminal_type = models.IntegerField(u'终端类型', blank=True, default=0, choices=TERMINAL_TYPE)
    release_note = models.CharField(u'说明', max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s' % self.version

    class Meta:
        verbose_name = u'版本管理'
        verbose_name_plural = u'版本管理'

