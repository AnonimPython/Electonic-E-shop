from django.urls import path
from .views import OrderCreateView, OrderHistoryView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='api_order_create'),
    path('history/', OrderHistoryView.as_view(), name='api_order_history'),
]