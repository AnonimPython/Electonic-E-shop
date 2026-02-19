from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Добавляем поле balance в отображение
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('balance',)}),
    )
    list_display = ('username', 'email', 'balance', 'is_staff')

admin.site.register(User, CustomUserAdmin)