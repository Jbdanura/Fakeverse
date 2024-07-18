from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from posts.models import Post
def allusers_view(request):
    users = User.objects.all()
    return render(request, "users/allusers.html",{"users":users})



@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'users/profile.html', {'profile': profile, 'posts': posts})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})


def search_user(request):
    query = request.GET.get('query')
    if query:
        user = User.objects.filter(username__iexact=query).first()
        if user:
            return redirect('view_profile', user.username)
        else:
            return render(request, 'user_not_found.html')
    return redirect('home')