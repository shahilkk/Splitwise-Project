from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from web.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.core.mail import send_mail
from django.http import HttpResponse

from django.db.models import Sum, Case, When, F, DecimalField, Value
from rest_framework.response import Response  

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
        expense_type = serializer.validated_data['expense_type']
        total_amount = serializer.validated_data['total_amount']
        participants = serializer.validated_data['participants']
        paid_by = serializer.validated_data['paid_by']
        name = serializer.validated_data['name']
        print(paid_by,'paid_by')
        paid_user=User.objects.get(id=paid_by.id)
        # print(participants.set(),'participants.set()')
        group = serializer.validated_data['group']
        expense_entry=Expense(group=group,total_amount=total_amount,expense_type=expense_type,paid_by=paid_user)
        expense_entry.save()
        expense_entry.participants.set(participants)

        percentage_shares = serializer.validated_data.get('percentage_shares')
        print(percentage_shares,'!'*20)
        print(expense_type,'&'*10)
        if expense_type == 'EQUAL':   
       
            share_per_participant = total_amount / len(participants)
            serializer.validated_data['share_per_participant'] = share_per_participant
            # Create a Transaction for each participant
            for participant in participants:
                print(participant,'*'*10)
                print(participant.id,'#'*10)
                get_user=User.objects.get(id=participant.id)
                print(get_user,'get_user')
                print(expense_entry,'I'*10)
                print(expense_entry.id,'j'*10)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount += share_per_participant
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=share_per_participant,
                            status=False,
                            Lender=paid_user
        )
              
               
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
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount += amount
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=amount,
                            status=False,
                            Lender=paid_user
                            )
              
        if expense_type == 'EXACT':
            print(percentage_shares,'percentage_sharespercentage_sharespercentage_sharespercentage_shares')
            if not percentage_shares or sum(percentage_shares) != total_amount:
                raise serializers.ValidationError("percentage_shares must be provided and sum up to the total amount.")
        

            for share, participant in zip(percentage_shares, participants):
                get_user = User.objects.get(id=participant.id)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount += share
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=share,
                            status=False,
                            Lender=paid_user
                            )
            
        # send_email(paid_user, get_user)
        # print(participants.id,'#'*20)
        
        # print(paid_user.id,'#'*20)
        for mail_user in participants:
            send_email(mail_user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import action
# from rest_framework.response import Response
# # from .models import Group, Transaction, Expense
# from .serializers import ExpenseSerializer
# from collections import defaultdict
# from rest_framework import viewsets
# from decimal import Decimal



# class SimplifyViewSet(ModelViewSet):
#     print('new'*10)
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

#     @action(detail=True, methods=['post'])
#     def simplify_expenses(self, request, pk=None):
#         group = get_object_or_404(Group, pk=pk)
#         print(group,'group')
#         if group.simplify_expenses:
#             transactions = Transaction.objects.filter(group=group)
#             print(transactions,'transactions')
#             balances = defaultdict(Decimal)
#             print(balances,'balances')
#             for transaction in transactions:
#                 balances[transaction.paid_to] += transaction.amount
#                 balances[transaction.user] -= transaction.amount
#                 # print(balances[transaction.paid_to],'balances[transaction.paid_to]')
#                 # print(balances[transaction.user],'balances[transaction.user]')

#             for user, balance in balances.items():
#                 print(user,balance)
#                 if balance > 0:
#                     simplified_expense = Expense.objects.create(
#                         group=group,
#                         name=f"Simplified Expense for {user}",
#                         expense_type='EXACT',
#                         total_amount=balance,
#                         paid_by=user,
#                         status=True
#                     )
#                     recipient = min(balances, key=balances.get)
#                     Transaction.objects.create(
#                         group=group,
#                         user=user,
#                         paid_to=recipient,
#                         amount=balance,
#                         status=True
#                     )
#                 elif balance < 0:
#                     simplified_expense = Expense.objects.create(
#                         group=group,
#                         name=f"Simplified Expense for {user}",
#                         expense_type='EXACT',
#                         total_amount=-balance,
#                         paid_by=recipient,
#                         status=True
#                     )
#                     Transaction.objects.create(
#                         group=group,
#                         user=recipient,
#                         paid_to=user,
#                         amount=-balance,
#                         status=True
#                     )

#             return Response({'message': 'Expenses simplified successfully'})
#         else:
#             return Response({'message': 'Simplify expenses is not enabled for this group'}, status=status.HTTP_400_BAD_REQUEST)



class PaidViewSet(ModelViewSet):
    queryset = Paid.objects.all()
    serializer_class = PaidSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        paid_type = serializer.validated_data['paid_type']
        total_amount = serializer.validated_data['total_amount']
        participants = serializer.validated_data['participants']
        paid_by = serializer.validated_data['user']
        expense = serializer.validated_data['expense']
        # name = serializer.validated_data['name']
        print(paid_by,'paid_by')
        paid_user=User.objects.get(id=paid_by.id)
        expense_id=Expense.objects.get(id=expense.id)
        # print(participants.set(),'participants.set()')
        group = serializer.validated_data['group']
        paid_entry=Paid(group=group,total_amount=total_amount,paid_type=paid_type,user=paid_user,expense=expense_id)
        paid_entry.save()
        paid_entry.participants.set(participants)

        percentage_shares = serializer.validated_data.get('percentage_shares')
        print(percentage_shares,'!'*20)
        print(paid_type,'&'*10)
        if paid_type == 'EQUAL':   
       
            share_per_participant = total_amount / len(participants)
            serializer.validated_data['share_per_participant'] = share_per_participant
            # Create a Transaction for each participant
            for participant in participants:
                print(participant,'*'*10)
                print(participant.id,'#'*10)
                get_user=User.objects.get(id=participant.id)
                print(get_user,'get_user')
                # print(expense_entry,'I'*10)
                # print(expense_entry.id,'j'*10)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount -= share_per_participant
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=share_per_participant,
                            status=False,
                            Lender=paid_user
                            )  
              
               
        if paid_type == 'PERCENT':
            
            
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
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount -= amount
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=amount,
                            status=False,
                            Lender=paid_user
                            )
              
        if paid_type == 'EXACT':
            print(percentage_shares,'percentage_sharespercentage_sharespercentage_sharespercentage_shares')
            if not percentage_shares or sum(percentage_shares) != total_amount:
                raise serializers.ValidationError("percentage_shares must be provided and sum up to the total amount.")
        

            for share, participant in zip(percentage_shares, participants):
                get_user = User.objects.get(id=participant.id)
                with transaction.atomic():
                    try:
                        existing_transaction = Transaction.objects.get(group=group, Borrower=get_user,Lender=paid_user)
                        existing_transaction.amount -= share
                        existing_transaction.save()
                    except Transaction.DoesNotExist:
                        Transaction.objects.create(
                            group=group,
                            Borrower=get_user,
                            amount=share,
                            status=False,
                            Lender=paid_user
                            )
            
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)








# class TransactionViewSet(ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     def list(self, request):
#         user_pk = request.query_params.get('user_pk')
#         user_transactions_pay = Transaction.objects.filter(paid_to=user_pk)
#         user_transactions_get = Transaction.objects.filter(user=user_pk)

#         total_amount_to_pay = user_transactions_pay.aggregate(Sum('amount'))['amount__sum'] or 0
#         total_amount_to_get = user_transactions_get.aggregate(Sum('amount'))['amount__sum'] or 0

#         balance_data = Transaction.objects.values('user').annotate(
#             balance=Sum(models.Case(
#                 models.When(paid_to=user_pk, then=-models.F('amount')),
#                 default=models.F('amount'),
#                 output_field=models.DecimalField(max_digits=10, decimal_places=2)
#             ))
#         )

#         return Response({
#             'user_transactions_pay': TransactionSerializer(user_transactions_pay, many=True).data,
#             'user_transactions_get': TransactionSerializer(user_transactions_get, many=True).data,
#             'total_amount_to_pay': total_amount_to_pay,
#             'total_amount_to_get': total_amount_to_get,
#             'balances': balance_data,
#         })


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request):
        user_pk = request.query_params.get('user_pk')
        print(user_pk,'user_pk')
        user_transactions_Lender = Transaction.objects.filter(Lender=user_pk)
        user_transactions_Borrower = Transaction.objects.filter(Borrower=user_pk)

        total_amount_to_get = user_transactions_Lender.aggregate(Sum('amount'))['amount__sum'] or 0
        total_amount_to_pay = user_transactions_Borrower.aggregate(Sum('amount'))['amount__sum'] or 0

        balance_data = Transaction.objects.values('Lender').annotate(
            balance=Sum(models.Case(
                models.When(Lender=user_pk, then=-models.F('amount')),
                default=models.F('amount'),
                output_field=models.DecimalField(max_digits=10, decimal_places=2)
            ))
        )

        return Response({
            'user_transactions_Lender': TransactionSerializer(user_transactions_Lender, many=True).data,
            'user_transactions_Borrower': TransactionSerializer(user_transactions_Borrower, many=True).data,
            'total_amount_to_pay_Borrowered': total_amount_to_pay,
            'total_amount_to_get_Lended': total_amount_to_get,
            'balances': balance_data,
        })





# def send_email():
#     subject = 'Hello, Django Email!'
#     message = 'This is a test email sent from a Django application.'
#     from_email = 'shahilkhan.7139@gmail.com'
#     recipient_list = ['shahilkhanarimbra@gmail.com']

#     send_mail(subject, message, from_email, recipient_list)
#     return HttpResponse('Email sent successfully')
from django.http import JsonResponse
import json

from django.template import loader

def User_wise_Details(user_pk):

    results = []
    user_balances = calculate_user_balances(user_pk)
    results.append({'User ID': user_pk, 'Balances': user_balances})

    # print(results,'results')
    return JsonResponse({'Balances for All Users': results})

def calculate_user_balances(user_pk):
    user_transactions_Lender = Transaction.objects.filter(Lender=user_pk)
    user_transactions_Borrower = Transaction.objects.filter(Borrower=user_pk)

    total_amount_to_get = user_transactions_Lender.aggregate(Sum('amount'))['amount__sum'] or 0
    total_amount_to_pay = user_transactions_Borrower.aggregate(Sum('amount'))['amount__sum'] or 0

    # Convert QuerySets to lists of dictionaries
    user_transactions_Lender_list = list(user_transactions_Lender.values())
    user_transactions_Borrower_list = list(user_transactions_Borrower.values())

    balance_data = Transaction.objects.values('Lender').annotate(
        balance=Sum(
            Case(
                When(Lender=user_pk, then=-F('amount')),
                default=F('amount'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )

    return {
        'user_transactions_Lender': user_transactions_Lender_list,
        'user_transactions_Borrower': user_transactions_Borrower_list,
        'total_amount_to_pay_Borrowered': total_amount_to_pay,
        'total_amount_to_get_Lended': total_amount_to_get,
        # 'balances': list(balance_data),  # Convert balance_data to a list
    }


def send_email(user_pk):
    value=User_wise_Details(user_pk)
    user_details=User.objects.get(id=user_pk)
    # print(user_details.email)
    # json_content = value.json().get('key')
    
    Content = value.content.decode('utf-8')  
    json_data = json.loads(Content)

    # to_json=Content.json()
    # print(json_data)
    # print(json_data)
    user_transactions_lender = json_data['Balances for All Users'][0]['Balances']['user_transactions_Lender']
    user_transactions_Borrower = json_data['Balances for All Users'][0]['Balances']['user_transactions_Borrower']
    total_amount_to_pay_Borrowered = json_data['Balances for All Users'][0]['Balances']['total_amount_to_pay_Borrowered']
    total_amount_to_get_Lended = json_data['Balances for All Users'][0]['Balances']['total_amount_to_get_Lended']

    # print(type(total_amount_to_pay_Borrowered))

    # Load the email template from a file
    with open('templates/emailnotification.html', 'r') as f:
        template_str = f.read()

    Borrower = []
    # print(user_transactions_lender,'user_transactions_lender')
    for Single_transaction in user_transactions_lender:
        transaction = Transaction.objects.get(id=Single_transaction['id'])
        borrower_name = transaction.Borrower.username  # Assuming you have a 'username' field in the User model

        transaction_data = {
        'Borrower_Name': borrower_name,
        'Amount': transaction.amount,
            }

        Borrower.append(transaction_data)

    Lender=[]
    # print(user_transactions_Borrower,'user_transactions_Borrower')
    for Single_transaction in user_transactions_Borrower:
        transaction = Transaction.objects.get(id=Single_transaction['id'])
        Lender_name = transaction.Lender.username  # Assuming you have a 'username' field in the User model

       
        transaction_data = {
        'Lender_Name': Lender_name,
        'Amount': transaction.amount,
            }

        Lender.append(transaction_data)
    # print(Borrower,'BorrowerBorrower')
    # Render the email template with data
    template = loader.get_template('emailnotification.html')
    rendered_message = template.render(
        {
            'data': 'Auto Verification of Bank accounts and GST for newly added Business Partners has been terminated due to insufficient funds in Cashfree wallet. Kindly top-up the wallet to resume Auto Verification',
            # 'result_Data':json_data,
            "total_amount_to_pay_Borrowered":"{:.2f}".format(float(total_amount_to_pay_Borrowered)),
            "total_amount_to_get_Lended":"{:.2f}".format(float(total_amount_to_get_Lended)),
            "Borrower":Borrower,
            "Lender":Lender
            
            }
        )
    # print(Lender,'Borrower_NameBorrower_Name')
    # Define email parameters
    subject = f"Splitwise Transaction Summary{user_details.first_name}"
    message = ''
    from_email = 'shahilkhan.7139@gmail.com'
    recipient_list = [user_details.email]

    # Send the email
    send_mail(subject, message, from_email, recipient_list, html_message=rendered_message)

    return HttpResponse('Alert message sent')