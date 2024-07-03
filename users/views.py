from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def allusers_view(request):
    users = User.objects.all()
    return render(request, "users/allusers.html",{"users":users})




