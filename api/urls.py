# from django.urls import path

# from . import views
from rest_framework.routers  import DefaultRouter
# from rest_framework_nested import routers

# router = routers.DefaultRouter()
# router.register('Group', views.GroupViewSet)
# router.register('Expense', views.ExpenseViewSet)
# urlpatterns=router.urls 

from django.urls import path, include
from rest_framework import routers
from . import views

# Define your custom path for simplifying expenses
custom_urlpatterns = [
    # path('Group/<int:pk>/simplify_expenses/', views.SimplifyViewSet.as_view({'post': 'simplify_expenses'}), name='group-simplify-expenses')
    # path('month-wise/', views.Month_wise, name='month_wise'),
]

# Use DefaultRouter to handle the standard routes
router = routers.DefaultRouter()

# Register the view for the 'Group' model
router.register('Group', views.GroupViewSet)
router.register('Expense', views.ExpenseViewSet)
router.register('Paid', views.PaidViewSet)
router.register('Transactions', views.TransactionViewSet)


# Combine the custom path with the DefaultRouter URLs
urlpatterns = [
    *router.urls,
    *custom_urlpatterns,
]