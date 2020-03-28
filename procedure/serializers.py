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
    class Meta:
        model = Task
        fields = "__all__"

