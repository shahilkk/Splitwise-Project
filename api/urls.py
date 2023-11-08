from django.urls import path

from . import views
from rest_framework.routers  import DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('Group', views.GroupViewSet)
router.register('Expense', views.ExpenseViewSet)
urlpatterns=router.urls 