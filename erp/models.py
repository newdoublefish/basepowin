from django.db import models


# Create your models here.
class MF_MO(models.Model):
    MO_NO = models.CharField(u'制定单号', max_length=20, primary_key=True)
    SO_NO = models.CharField(u'受订单号', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'MF_MO'
        verbose_name = u'制定单'
        verbose_name_plural = u'制定单'

    def __str__(self):
        return self.MO_NO


# Create your models here.
class MF_TZ(models.Model):
    TZ_NO = models.CharField(u'通知单号', max_length=20, primary_key=True)
    MO_NO = models.CharField(u'制定单号', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'MF_TZ'
        verbose_name = u'通知单'
        verbose_name_plural = u'通知单'

    def __str__(self):
        return self.MO_NO


