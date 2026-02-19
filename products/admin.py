from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    inlines = [ProductImageInline]