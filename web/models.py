from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractUser
)
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(default=0, null=True, max_length=15)



class Group(models.Model):
    name = models.CharField(max_length=100)
    Added_date = models.DateField(auto_now_add=True)
    simplify_expenses = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Expense(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='expenses_paid')
    participants = models.ManyToManyField(User)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Transaction(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    Borrower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='give_money_to')
    Lender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='get_money_from')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} - {self.Borrower.first_name} -To-{self.Lender.first_name} - {self.amount}"
        

class Paid(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    paid_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_user')
    participants = models.ManyToManyField(User,related_name='tobe_paid')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name