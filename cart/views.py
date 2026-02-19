from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

#* REST API 
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CartSerializer, CartItemSerializer


#* REST API 
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#* Веб-интерфейс
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Товар добавлен в корзину')
        return redirect('cart_detail')
    return redirect('product_list')

@login_required
def cart_update(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Товар удалён из корзины')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено')
    return redirect('cart_detail')

@login_required
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удалён из корзины')
    return redirect('cart_detail')


