from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem

#* REST API
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .serializers import OrderSerializer

#* REST API
class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка остатков и баланса
        total = 0
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return Response({'error': f'Not enough stock for {item.product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            total += item.product.price * item.quantity

        if request.user.balance < total:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание заказа
        order = Order.objects.create(user=request.user, total_amount=total)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            # Списание со склада
            item.product.stock -= item.quantity
            item.product.save()

        # Списание баланса
        request.user.balance -= total
        request.user.save()

        # Очистка корзины
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.orders.all()

#* Веб-интерфейс
@login_required
def order_create(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Корзина пуста')
        return redirect('cart_detail')

    # Проверка остатков и баланса
    total = 0
    for item in cart.items.all():
        if item.quantity > item.product.stock:
            messages.error(request, f'Товара "{item.product.name}" недостаточно на складе')
            return redirect('cart_detail')
        total += item.product.price * item.quantity

    if request.user.balance < total:
        messages.error(request, 'Недостаточно средств на балансе')
        return redirect('cart_detail')

    # Создание заказа
    order = Order.objects.create(user=request.user, total_amount=total)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
        # Списание со склада
        item.product.stock -= item.quantity
        item.product.save()

    # Списание баланса
    request.user.balance -= total
    request.user.save()

    # Очистка корзины
    cart.items.all().delete()

    messages.success(request, 'Заказ успешно оформлен!')
    return redirect('order_history')

@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'orders/history.html', {'orders': orders})

