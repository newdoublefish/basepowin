from rest_framework import serializers
from .models import Mop, Procedure, Receipt, Task


class MopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mop
        fields = "__all__"


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = "__all__"


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('deliver_procedure', 'receiver_procedure', 'quantity')


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'sub_procedure', 'procedure', 'procedure_name', 'plan_quantity', 'quantity',
                  'weight', 'created_at', 'started_at', 'stopped_at', 'user', 'username', 'status', 'status_text')
        readonly = ('created_at', 'started_at', 'stopped_at'),

    def get_username(self, obj):
        if obj.user is not None:
            return obj.user.username
        return ""

    def get_status_text(self, obj):
        return obj.get_status_display()


