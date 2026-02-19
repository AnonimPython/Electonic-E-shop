from django.urls import path
from .views import CartDetailView, CartAddView, CartUpdateView, CartRemoveView

urlpatterns = [
    path('', CartDetailView.as_view(), name='api_cart'),
    path('add/', CartAddView.as_view(), name='api_cart_add'),
    path('update/', CartUpdateView.as_view(), name='api_cart_update'),
    path('remove/<int:item_id>/', CartRemoveView.as_view(), name='api_cart_remove'),
]