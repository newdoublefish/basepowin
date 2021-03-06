from .serializers import DepartmentSerializer, RoleSerializer, UserProfileSerializer
from .models import Department, Role, UserProfile
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        if self.request.user.dept is not None:
            return Department.objects.all(parent=self.request.user.dept)


class RoleViewSet(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_fields = ('name',)


def fill_user_permissions(user=None):
    role_list = user.role.all()
    user_permissions_set = {permissions for role in role_list for permissions in role.permissions.all()}
    user.user_permissions.clear()
    user.user_permissions.add(*user_permissions_set)
    user.save()


class UserProfileViewSet(GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_fields = ('role', 'dept',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = serializer.save()
                # 分配基于角色的权限
                fill_user_permissions(instance)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            transaction.savepoint_commit(save_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = serializer.save()
                fill_user_permissions(instance)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                raise e
            transaction.savepoint_commit(save_id)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            serializer = UserProfileSerializer(user)
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = request.META.get('REMOTE_ADDR')
            if user.is_active is True:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': serializer.data,
                })
            else:
                raise Exception("not active")
        except Exception as e:
            return Response({"status": "error", "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

