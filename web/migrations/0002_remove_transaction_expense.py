# Generated by Django 4.2.6 on 2023-11-08 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='expense',
        ),
    ]
