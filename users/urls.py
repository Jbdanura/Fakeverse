# urls.py
from django.urls import path
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from .views import *

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(form_class=CustomSignupForm), name='account_signup'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('search/', search_user, name='search_user'),
    path('follow/<str:username>/', follow_unfollow, name='follow'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('edit_avatar', edit_avatar, name='edit_avatar'),
    path('guest_login',guest_login, name="guest_login")
]