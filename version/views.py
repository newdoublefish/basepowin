from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
import coreapi
from .models import Version
from .serializers import VersionSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.
class VersionViewSet(GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    filterset_fields = ("version", "is_valid", "terminal_type")
    permission_classes = (AllowAny, )

    @action(detail=False, methods=['get'])
    def latest(self, request, pk=None):
        ter_type = self.request.query_params.get('terminal_type', None)
        if ter_type is not None:
            queryset = self.get_queryset().filter(terminal_type=ter_type, is_valid=True).order_by('-version')
        else:
            queryset = self.get_queryset().filter(is_valid=True).order_by('-version')
        if queryset.count() == 0:
            return Response({"status": "error", "msg": {}}, status=status.HTTP_200_OK)
        else:
            latest = queryset[0]
            serilizer_data = VersionSerializer(latest)
            # print(serilizer_data.data)
            return Response({"status": "success", "msg": serilizer_data.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def is_valid(self, request, pk=None):
        version = request.data.get('version', None)
        terminal = request.data.get('terminal_type', None)
        if version is None or terminal is None:
            return Response({"status": "error", "msg": "invalid"}, status=status.HTTP_200_OK)
        ver = self.get_queryset().filter(version=version, terminal_type=terminal, is_valid=True).first()
        if ver is not None:
            return Response({"status": "success", "msg": "valid"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "msg": "invalid"}, status=status.HTTP_200_OK)



