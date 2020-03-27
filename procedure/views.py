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
from .models import Mop, Procedure, Receipt, Task
from django.db import transaction
from django.utils import timezone
from . import common
import json


# 耗时操作，可以考虑放到异步中执行
def create_procedures(mop_instance=None):
    # create first procedure
    try:
        procedure1 = Procedure(name='裁线', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               quantity=mop_instance.quantity,
                               parent=None)
        procedure1.save()

        procedure2 = Procedure(name='打端子', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               quantity=mop_instance.quantity,
                               parent=procedure1)
        procedure2.save()

        procedure3 = Procedure(name='组装', mop=mop_instance, part_no_name=mop_instance.part_no_name,
                               mop_name=mop_instance.manufacture_order_name,
                               quantity=mop_instance.quantity,
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

    @action(detail=True, methods=['get'])
    def reset(self, request, pk=None):
        pass


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
        pass

    @action(detail=True, methods=['get'])
    def finish(self, request, pk=None):
        pass

    @action(detail=True, methods=['get'])
    def reset(self, request, pk=None):
        pass


def fill_receipt(receipt=None):
    if receipt.receiver_procedure.mop != receipt.deliver_procedure.mop:
        raise Exception("不在一个制定单内的两个工序")
    receipt.deliver_procedure_name = receipt.deliver_procedure.name
    receipt.receiver_procedure_name = receipt.receiver_procedure.name
    # 正常
    if receipt.deliver_procedure == receipt.receiver_procedure.parent:
        receipt.deliver_type = 1
    # 反工
    elif receipt.deliver_procedure.parent == receipt.receiver_procedure:
        receipt.deliver_type = 2
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
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
            receipt.deliver = request.user
            receipt.status = common.RECEIPT_STATUS_DELIVERED
            receipt.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def receive(self, request, pk=None):
        try:
            receipt = self.get_object()
            if receipt.status != common.RECEIPT_STATUS_DELIVERED:
                raise Exception("该接收单处于%s状态" % receipt.get_status_display())
            receipt.received_at = timezone.now()
            receipt.receiver = request.user
            receipt.status = common.RECEIPT_STATUS_RECEIVED
            receipt.save()
        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "success", "data": {}}, status=status.HTTP_200_OK)


class TaskViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ('procedure',)

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        pass

    @action(detail=True, methods=['get'])
    def finish(self, request, pk=None):
        pass
