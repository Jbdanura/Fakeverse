# urls.py
from django.urls import path
from allauth.account.views import SignupView
from .forms import CustomSignupForm

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(form_class=CustomSignupForm), name='account_signup'),
]