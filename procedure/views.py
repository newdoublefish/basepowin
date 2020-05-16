from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import FilterSet
import django_filters
from .serializers import MopSerializer, ProcedureSerializer, ReceiptSerializer, TaskSerializer
from .models import Mop, Procedure, Receipt, Task, ReceiveHistory
from django.db import transaction
from django.utils import timezone
from . import common
from xadmin.views.base import BaseAdminView, ModelAdminView, filter_hook, csrf_protect_m
import collections
from xadmin.views import Dashboard

import json


# 耗时操作，可以考虑放到异步中执行
def create_procedures(mop_instance=None):
    # create first procedure
    try:
        procedure1 = Procedure(name='裁线', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               parent=None)
        procedure1.save()

        procedure2 = Procedure(name='打端子', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               parent=procedure1)
        procedure2.save()

        procedure3 = Procedure(name='组装', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               parent=procedure2)
        procedure3.save()
    except Exception as e:
        raise e


class MopViewSet(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Mop.objects.all()
    serializer_class = MopSerializer
    filterset_fields = ('manufacture_order_name',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO:判断有没有重名的，已经完成的制订单不会再生成了
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = serializer.save()
                # TODO：创建流程
                create_procedures(instance)

                print(instance.id)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProcedureViewSet(GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    filterset_fields = ('mop',)

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.status is not common.PROCEDURE_STATUS_UN_START:
                raise Exception("该工序处于%s状态" % instance.get_status_display())
            instance.status = common.PROCEDURE_STATUS_UNDER_GOING
            instance.dept = request.user.dept
            instance.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def finish(self, request, pk=None):
        try:
            instance = self.get_object()
            if instance.status is not common.PROCEDURE_STATUS_UNDER_GOING:
                raise Exception("该工序处于%s状态" % instance.get_status_display())
            instance.status = common.PROCEDURE_STATUS_FINISHED
            instance.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def reset(self, request, pk=None):
        pass

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = self.get_object()
                instance.received_quantity = instance.received_quantity + request.data['quantity']
                instance.save()

                history = ReceiveHistory()
                history.receiver_procedure = instance
                history.receiver = request.user
                history.quantity = request.data['quantity']
                history.save()

            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        return Response({"status": "success", "data": self.get_serializer(instance).data}, status=status.HTTP_200_OK)


def fill_receipt(receipt=None):
    if receipt.receiver_procedure.mop != receipt.deliver_procedure.mop:
        raise Exception("不在一个制定单内的两个工序！")
    receipt.deliver_procedure_name = receipt.deliver_procedure.name
    receipt.receiver_procedure_name = receipt.receiver_procedure.name
    # 正常
    if receipt.deliver_procedure == receipt.receiver_procedure.parent:
        receipt.deliver_type = 1
    # 反工
    elif receipt.deliver_procedure.parent == receipt.receiver_procedure:
        receipt.deliver_type = 2
    else:
        raise Exception("只能在相邻工序间交接！")
    receipt.create_at = timezone.now()
    receipt.save()


class ReceiptViewSet(GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filterset_fields = ('deliver_procedure', 'receiver_procedure')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                fill_receipt(instance)
                print(instance.id)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def deliver(self, request, pk=None):
        try:
            receipt = self.get_object()
            if receipt.status != common.RECEIPT_STATUS_UN_KNOW:
                raise Exception("该接收单处于%s状态" % receipt.get_status_display())

            receipt.delivered_at = timezone.now()
            print(request.user, self.request.user)
            receipt.deliver = request.user
            receipt.status = common.RECEIPT_STATUS_DELIVERED
            receipt.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def receive(self, request, pk=None):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                receipt = self.get_object()
                if receipt.status != common.RECEIPT_STATUS_DELIVERED:
                    raise Exception("该接收单处于%s状态" % receipt.get_status_display())
                receipt.received_at = timezone.now()
                receipt.receiver = request.user
                receipt.status = common.RECEIPT_STATUS_RECEIVED
                receipt.deliver_procedure.delivered_quantity += receipt.quantity
                receipt.deliver_procedure.save()
                receipt.receiver_procedure.received_quantity += receipt.quantity
                receipt.receiver_procedure.save()
                receipt.receiver = request.user
                receipt.save()
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)


# 调价判断应该反倒serializer来做
def fill_task(task=None):
    task.procedure_name = task.procedure.name
    task.status = common.TASK_STATUS_UN_START
    if task.procedure.status is not common.PROCEDURE_STATUS_UNDER_GOING:
        raise Exception("该工序处于%s状态" % task.procedure.get_status_display())
    if task.user is None:
        raise Exception("请分配操作人员")
    if task.quantity <= 0:
        raise Exception("数量必须大于0")
    task.save()


class TaskViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ('procedure', 'status')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                fill_task(instance)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.started_at = timezone.datetime.now()
            instance.status = common.TASK_STATUS_UNDER_GOING
            instance.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def finish(self, request, pk=None):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = self.get_object()
                instance.procedure.quantity += instance.quantity
                instance.procedure.save()

                instance.stopped_at = timezone.datetime.now()
                instance.status = common.TASK_STATUS_FINISHED
                instance.save()
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)


# Create your views here.
class ProcedureDetail(Dashboard, BaseAdminView):
    template_name = 'procedure/procedure.html'

    @filter_hook
    def get_context(self):
        context = Dashboard.get_context(self)
        # render_data = {
        #     "mop": "",
        #     "procedures": []
        # }
        mop = Mop.objects.get(id=int(self.request.GET.get('id')))
        # render_data['mop'] = MopSerializer(mop).data
        context['title'] = "制订单号:" + mop.manufacture_order_name
        procedures = Procedure.objects.filter(mop=mop).all().order_by("created_at")
        # if procedures.exists() is True:
        #     for procedure in procedures:
        #         render_data['procedures'].append(ProcedureSerializer(procedure).data)

        # render_data['mop'] = mop
        # render_data['procedures'] = procedures
        # context['data'] = render_data
        context['mop'] = mop
        context['procedures'] = procedures
        return context

    def get(self, request, *args, **kwargs):
        return self.template_response(self.template_name, self.get_context())
