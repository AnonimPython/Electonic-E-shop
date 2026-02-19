from django.urls import path
from .views import RegistrationView, ProfileView, DepositView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='api_register'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('deposit/', DepositView.as_view(), name='api_deposit'),
]