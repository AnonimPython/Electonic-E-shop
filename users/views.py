from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, DepositForm

# REST Framework imports
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

#* REST API 
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.balance += amount
        user.save(update_fields=['balance'])
        return Response({'new_balance': user.balance}, status=status.HTTP_200_OK)

#* Веб-интерфейс
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance += amount
            request.user.save()
            messages.success(request, f'Баланс пополнен на {amount} руб.')
            return redirect('profile')
    else:
        form = DepositForm()
    return render(request, 'users/profile.html', {'form': form})


