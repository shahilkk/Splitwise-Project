from web.models import *
from django.http import HttpResponse

from celery import shared_task 

from time import sleep
from .views import send_email

   


@shared_task(blind=True)
def Daily_mailgeneration():
    getuser=User.objects.all()
    for single_user in getuser:
        send_email(single_user.id)
        sleep(1)
    return "Task Complete!"