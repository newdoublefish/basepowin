from django.shortcuts import render
from .serializers import DepartmentSerializer, RoleSerializer, UserProfileSerializer
from .models import Department, Role, UserProfile
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone


# Create your views here.
class DepartmentViewSet(GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ('name', 'parent')


class RoleViewSet(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_fields = ('name',)


class UserProfileViewSet(GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_fields = ('role', 'dept',)


