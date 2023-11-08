from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from web.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction



# Create your views here.
class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]



class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        
        expense_type = serializer.validated_data['expense_type']
        total_amount = serializer.validated_data['total_amount']
        participants = serializer.validated_data['participants']
        name = serializer.validated_data['name']
        print(participants,'participants')
        # print(participants.set(),'participants.set()')
        group = serializer.validated_data['group']
        # user = get_user
        expense_entry=Expense(group=group,total_amount=total_amount,expense_type=expense_type,name=name)
        expense_entry.save()
        expense_entry.participants.set(participants)

        # print(new,'newnewnewnewnewnewnewnewnewnewnewnew')
        percentage_shares = serializer.validated_data.get('percentage_shares')
        print(percentage_shares,'!'*20)
        print(expense_type,'&'*10)
        if expense_type == 'EQUAL':   
            # new=Expense(group=serializer.validated_data['group'],total_amount=total_amount,expense_type=expense_type,name=name)
            # new.save()         
            share_per_participant = total_amount / len(participants)
            serializer.validated_data['share_per_participant'] = share_per_participant
            # Create a Transaction for each participant
            for participant in participants:
                print(participant,'*'*10)
                print(participant.id,'#'*10)
                get_user=User.objects.get(id=participant.id)
                print(get_user,'get_user')
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, user=get_user)
                        existing_transaction.amount += share_per_participant
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            user=get_user,
                            amount=share_per_participant,
                            status=False
        )
                # Transaction.objects.create(
                #     group=serializer.validated_data['group'],
                #     user=get_user,
                #     amount=share_per_participant,
                #     status=False
                # )             
                # 
               
        if expense_type == 'PERCENT':
            
            
            if not percentage_shares or sum(percentage_shares) != 100:
                raise serializers.ValidationError("Percentage shares must be provided and sum up to 100.")
            
            # print(percentage_share,'@'*10)
            for percentage_share, participant in zip(percentage_shares, participants):
                print(percentage_share,'I'*12)
                # print('0'*10)
                amount = (percentage_share / 100) * total_amount
                print(amount,'amount')
                get_user=User.objects.get(id=participant.id)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, user=get_user)
                        existing_transaction.amount += amount
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            user=get_user,
                            amount=amount,
                            status=False
                            )
                # Transaction.objects.create(
                #     group=serializer.validated_data['group'],
                #     user=get_user,
                #     amount=amount,
                #     status=False
                # )
                # response = super().create(request, *args, **kwargs)  
        if expense_type == 'EXACT':
            print(percentage_shares,'percentage_sharespercentage_sharespercentage_sharespercentage_shares')
            if not percentage_shares or sum(percentage_shares) != total_amount:
                raise serializers.ValidationError("percentage_shares must be provided and sum up to the total amount.")
        

            for share, participant in zip(percentage_shares, participants):
                get_user = User.objects.get(id=participant.id)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, user=get_user)
                        existing_transaction.amount += share
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            user=get_user,
                            amount=share,
                            status=False
                            )
                # Transaction.objects.create(
                #     group=serializer.instance.group,
                #     expense=serializer.instance,
                #     user=get_user,
                #     amount=share,
                #     status=False
                # )
        # super().create(request, *args, **kwargs)  
        # print(response,'responseresponseresponse')
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



