
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
    percentage_shares = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    # shares = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)


    class Meta:
        model = Expense
        fields = ['group','name','expense_type','total_amount','participants', 'percentage_shares','paid_by']

    # def validate(self, data):
    #     expense_type = data.get('expense_type')
    #     percentage_shares = data.get('percentage_shares')

    #     if expense_type == 'PERCENT':
    #         if not percentage_shares or sum(percentage_shares) != 100:
    #             raise serializers.ValidationError("Percentage shares must be provided and sum up to 100.")

    #     return data

    # def create(self, validated_data):
    #     expense_type = validated_data.get('expense_type')
    #     total_amount = validated_data.get('total_amount')
    #     # participants = validated_data.get('participants')
    #     name = validated_data.get('name')
    #     group = validated_data.get('group')
    #     percentage_shares = validated_data.get('percentage_shares')
    #     print(expense_type,'expense_type')
    #     new=Expense(group=group,total_amount=total_amount,expense_type=expense_type,name=name)
    #     new.save()
    #     print(new,'newnew')
        # Transaction.objects.create(
        #             group=validated_data['group'],
        #             user_id=participant_id,
        #             amount=amount,
        #             status=False
        #         )

        # return super().create(validated_data)










class PaidSerializer(serializers.ModelSerializer):
    percentage_shares = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    # shares = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)


    class Meta:
        model = Paid
        fields = ['group','expense','paid_type','total_amount','participants', 'percentage_shares','user']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'