from django.db import models
from user.models import Department, UserProfile


# Create your models here.
class Mop(models.Model):
    STATUS_CHOICES = (
        (0, '未开始'),
        (1, '进行中'),
        (2, '已结束'),
    )

    sell_order_name = models.CharField(u'受订单', max_length=32, null=True, blank=True)
    sell_order = models.IntegerField(u'受订单ID', null=True, blank=True)
    manufacture_order_name = models.CharField(u'制订单', max_length=32, null=True, blank=True)
    manufacture_order = models.IntegerField(u'制订单ID', null=True, blank=True)
    part_no_name = models.CharField(u'图号', max_length=32, null=True, blank=True)
    part_no = models.IntegerField(u'图号ID', null=True, blank=True)
    quantity = models.IntegerField(u'数量', null=True, blank=True)
    status = models.IntegerField(u"状态", choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(u'创建时间', null=True, blank=True)
    updated_at = models.DateTimeField(u'更新时间', null=True, blank=True)

    def __str__(self):
        return "%s" % self.manufacture_order_name

    class Meta:
        verbose_name = "制订单流程"
        verbose_name_plural = "制订单流程"


class Procedure(models.Model):
    STATUS_CHOICES = (
        (0, '未开始'),
        (1, '进行中'),
        (2, '已完成'),
    )
    name = models.CharField(u'工序', max_length=32, null=True, blank=True)
    mop = models.ForeignKey(Mop, verbose_name="制订单流程", on_delete=models.DO_NOTHING, null=True)
    mop_name = models.CharField(u'制订单流程', max_length=32, null=True, blank=True)
    part_no_name = models.CharField(u'图号', max_length=32, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, verbose_name='上一个工序', null=True, blank=True, )
    dept = models.ForeignKey(Department, verbose_name="部门", blank=True, null=True, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(u'数量', null=True, blank=True)
    status = models.IntegerField(u"状态", choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(u'创建时间', null=True, blank=True)
    updated_at = models.DateTimeField(u'更新时间', null=True, blank=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "工序"
        verbose_name_plural = "工序"


class Receipt(models.Model):
    STATUS_CHOICES = (
        (0, '未开始'),
        (1, '已发送'),
        (2, '已接收'),
    )
    dept = models.ForeignKey(Department, verbose_name="部门", blank=True, null=True, on_delete=models.DO_NOTHING)
    deliver_procedure = models.ForeignKey(Procedure, verbose_name="发送工序", blank=True, null=True,
                                          on_delete=models.DO_NOTHING, related_name="deliver_procedure")
    deliver_procedure_name = models.CharField(u'发送工序', max_length=32, null=True, blank=True)
    receiver_procedure = models.ForeignKey(Procedure, verbose_name="接收工序", blank=True, null=True,
                                           on_delete=models.DO_NOTHING, related_name="receiver_procedure")
    receiver_procedure_name = models.CharField(u'接收工序', max_length=32, null=True, blank=True)
    quantity = models.IntegerField(u'交接数量', null=True, blank=True)
    deliver = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="发单人员", null=True,
                                related_name="deliver")
    deliver_at = models.DateTimeField(u'发单时间', null=True, blank=True)
    receiver = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="签单人员", null=True,
                                 related_name="receiver")
    receiver_at = models.DateTimeField(u'签单时间', null=True, blank=True, )
    status = models.IntegerField(u"状态", choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return "%s" % self.quantity

    class Meta:
        verbose_name = "交接单"
        verbose_name_plural = "交接单"


class Task(models.Model):
    name = models.CharField(u'名称', max_length=32, blank=True, null=True)
    sub_procedure = models.CharField(u'子工序', max_length=32, blank=True, null=True)
    procedure = models.ForeignKey(Procedure, verbose_name="工序", blank=True, null=True, on_delete=models.DO_NOTHING)
    procedure_name = models.CharField(u'工序', max_length=32, null=True, blank=True)
    quantity = models.IntegerField(u'完成数量', null=True, blank=True)
    total = models.IntegerField(u'总数量', null=True, blank=True)
    start_at = models.DateTimeField(u'开始时间', null=True, blank=True)
    stop_at = models.DateTimeField(u'停止时间', null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="检验人员", null=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
