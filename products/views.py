from django.shortcuts import render, get_object_or_404
from .models import Product
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра товаров (только чтение).
    Доступно всем пользователям (даже неавторизованным).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

