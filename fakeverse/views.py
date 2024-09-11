from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def health_check(request):
    user = User.objects.get(username="machinegod")
    return HttpResponse("OK")