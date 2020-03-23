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
        # TODO:判断有没有重名的
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = serializer.save()
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


class ReceiptViewSet(GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filterset_fields = ('procedure',)


class TaskViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ('procedure',)
