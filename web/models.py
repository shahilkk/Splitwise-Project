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
    def __str__(self):
        return self.name

class Expense(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    participants = models.ManyToManyField(User)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Transaction(models.Model):
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} - {self.user.first_name} - {self.amount}"
        