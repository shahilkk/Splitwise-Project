
from web.models import *
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name','phone']



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name' ]

class ExpenseSerializer(serializers.ModelSerializer):
    Amount_Added = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    # shares = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)


    class Meta:
        model = Expense
        fields = ['group','name','expense_type','total_amount','participants', 'Amount_Added','paid_by']

   

class PaidSerializer(serializers.ModelSerializer):
    Amount_Added = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    # shares = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)


    class Meta:
        model = Paid
        fields = ['group','expense','paid_type','total_amount','participants', 'Amount_Added','user']


class TransactionSerializer(serializers.ModelSerializer):
    Borrower_name = serializers.CharField(source='Borrower.first_name', read_only=True)
    Lender_name = serializers.CharField(source='Lender.first_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'