from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label='Сумма пополнения')