from django.urls import path
from . import views


urlpatterns = [
    path('balance_transfer/', views.BalanceTransfer.as_view(), name='balance_transfer'),
]