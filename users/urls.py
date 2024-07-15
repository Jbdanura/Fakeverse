# urls.py
from django.urls import path
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from .views import *

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(form_class=CustomSignupForm), name='account_signup'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]