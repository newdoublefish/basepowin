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


class MopViewSet(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Mop.objects.all()
    serializer_class = MopSerializer
    filterset_fields = ('manufacture_order_name',)


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
